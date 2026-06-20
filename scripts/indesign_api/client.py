"""A dependency-free client for the Firefly Services InDesign API.

Only the Python standard library is used (urllib), so this runs anywhere without
``pip install``. Every endpoint on this API is asynchronous: you POST a job, get
a ``jobId`` + ``statusUrl`` back (HTTP 202), then poll the status URL until the
job reaches a terminal state (``succeeded``, ``partial_success``, or ``failed``).

The contract implemented here matches the OpenAPI spec documented in
instructions/indesign-automation/README.md.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any, Iterable

from .config import Config

TERMINAL_STATES = {"succeeded", "partial_success", "failed"}


class InDesignAPIError(RuntimeError):
    """Raised for transport/HTTP errors talking to the API or IMS."""

    def __init__(self, message: str, status: int | None = None, body: str = ""):
        super().__init__(message)
        self.status = status
        self.body = body


class JobFailedError(RuntimeError):
    """Raised when a job reaches the ``failed`` terminal state."""

    def __init__(self, message: str, event: dict[str, Any]):
        super().__init__(message)
        self.event = event


def _http(
    method: str,
    url: str,
    *,
    headers: dict[str, str],
    data: bytes | None = None,
    timeout: int = 60,
) -> tuple[int, dict[str, str], bytes]:
    """Perform an HTTP request, returning (status, headers, body bytes)."""
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as exc:  # 4xx/5xx
        body = exc.read()
        raise InDesignAPIError(
            f"{method} {url} failed: HTTP {exc.code}",
            status=exc.code,
            body=body.decode("utf-8", "replace"),
        ) from exc
    except urllib.error.URLError as exc:
        raise InDesignAPIError(f"{method} {url} failed: {exc.reason}") from exc


class InDesignClient:
    """High-level client for the Firefly Services InDesign API."""

    def __init__(self, config: Config):
        self.config = config
        self._token: str = ""
        self._token_expiry: float = 0.0

    # ------------------------------------------------------------------ auth
    def access_token(self) -> str:
        """Return a valid bearer token, minting one via IMS if needed."""
        if self.config.access_token:
            return self.config.access_token
        now = time.time()
        if self._token and now < self._token_expiry - 60:
            return self._token

        form = urllib.parse.urlencode(
            {
                "grant_type": "client_credentials",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "scope": self.config.scopes,
            }
        ).encode("utf-8")
        status, _headers, body = _http(
            "POST",
            self.config.ims_token_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=form,
        )
        payload = json.loads(body.decode("utf-8"))
        token = payload.get("access_token")
        if not token:
            raise InDesignAPIError(
                "IMS token response had no access_token", status=status,
                body=body.decode("utf-8", "replace"),
            )
        self._token = token
        self._token_expiry = now + float(payload.get("expires_in", 3600))
        return token

    def _headers(self, content_type: str | None = "application/json") -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.access_token()}",
            "x-api-key": self.config.client_id,
            "Accept": "application/json",
        }
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    # --------------------------------------------------------------- jobs
    def _post_job(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        """POST an async job, returning the 202 envelope ({jobId, statusUrl})."""
        url = f"{self.config.api_base}{path}"
        status, _headers, raw = _http(
            "POST", url, headers=self._headers(), data=json.dumps(body).encode("utf-8")
        )
        envelope = json.loads(raw.decode("utf-8")) if raw else {}
        if "statusUrl" not in envelope and "jobId" in envelope:
            envelope["statusUrl"] = f"{self.config.api_base}/v3/status/{envelope['jobId']}"
        return envelope

    def get_status(self, status_url: str) -> dict[str, Any]:
        """Fetch a single status event for a job."""
        if not status_url.startswith("http"):
            status_url = f"{self.config.api_base}{status_url}"
        _status, _headers, raw = _http("GET", status_url, headers=self._headers(None))
        return json.loads(raw.decode("utf-8"))

    def poll_job(
        self,
        status_url: str,
        *,
        interval: float = 3.0,
        timeout: float = 900.0,
        on_update=None,
    ) -> dict[str, Any]:
        """Poll a job until it reaches a terminal state.

        Returns the final status event. Raises JobFailedError on ``failed``.
        """
        deadline = time.time() + timeout
        last_state = None
        while True:
            event = self.get_status(status_url)
            state = event.get("status")
            if state != last_state and on_update:
                on_update(event)
            last_state = state
            if state in TERMINAL_STATES:
                if state == "failed":
                    raise JobFailedError(
                        f"Job failed: {event.get('errors')}", event=event
                    )
                return event
            if time.time() > deadline:
                raise InDesignAPIError(
                    f"Timed out after {timeout}s waiting for job (last state: {state})"
                )
            time.sleep(interval)

    def run(self, path: str, body: dict[str, Any], **poll_kwargs) -> dict[str, Any]:
        """Submit a job and block until it finishes; returns the final event."""
        envelope = self._post_job(path, body)
        status_url = envelope.get("statusUrl")
        if not status_url:
            raise InDesignAPIError(f"No statusUrl in job response: {envelope}")
        return self.poll_job(status_url, **poll_kwargs)

    # ----------------------------------------------------- request helpers
    @staticmethod
    def asset(url: str, destination: str | None = None) -> dict[str, Any]:
        """Build an input-asset entry (a pre-signed URL the API will download)."""
        entry: dict[str, Any] = {"source": {"url": url}}
        if destination:
            entry["destination"] = destination
        return entry

    @staticmethod
    def output(url: str, source: str, storage_type: str | None = None) -> dict[str, Any]:
        """Build an output-asset entry (a pre-signed PUT URL for the result)."""
        dest: dict[str, Any] = {"url": url}
        if storage_type:
            dest["storageType"] = storage_type
        return {"destination": dest, "source": source}

    # --------------------------------------------------------- endpoints
    def list_app_versions(self) -> Any:
        url = f"{self.config.api_base}/v3/app-versions"
        _status, _headers, raw = _http("GET", url, headers=self._headers(None))
        return json.loads(raw.decode("utf-8"))

    def list_custom_scripts(self, page: int = 0) -> Any:
        url = f"{self.config.api_base}/v3/scripts?page={int(page)}"
        _status, _headers, raw = _http("GET", url, headers=self._headers(None))
        return json.loads(raw.decode("utf-8"))

    def document_info(
        self,
        assets: Iterable[dict[str, Any]],
        target_document: str,
        *,
        links: bool = True,
        fonts: bool = True,
        page_items: bool = False,
        text_stories: bool = False,
        **poll_kwargs,
    ) -> dict[str, Any]:
        """Inspect an INDD/IDML: pages, links, fonts, page items, text stories."""
        body = {
            "assets": list(assets),
            "params": {
                "targetDocument": target_document,
                "pageInfo": {"enabled": True},
                "linkInfo": {"enabled": links},
                "fontInfo": {"enabled": fonts},
                "pageItemInfo": {"enabled": page_items},
                "textStoryInfo": {"enabled": text_stories},
            },
        }
        return self.run("/v3/document-info", body, **poll_kwargs)

    def create_rendition(
        self,
        assets: Iterable[dict[str, Any]],
        target_document: str,
        *,
        output_media_type: str = "application/pdf",
        outputs: Iterable[dict[str, Any]] | None = None,
        params: dict[str, Any] | None = None,
        **poll_kwargs,
    ) -> dict[str, Any]:
        """Render an InDesign document to PDF / PNG / JPEG."""
        merged_params: dict[str, Any] = {
            "targetDocuments": [target_document],
            "outputMediaType": output_media_type,
        }
        if params:
            merged_params.update(params)
        body: dict[str, Any] = {"assets": list(assets), "params": merged_params}
        if outputs:
            body["outputs"] = list(outputs)
        return self.run("/v3/create-rendition", body, **poll_kwargs)

    def data_merge(
        self,
        assets: Iterable[dict[str, Any]],
        target_document: str,
        data_source: str,
        *,
        output_media_type: str = "application/x-indesign",
        outputs: Iterable[dict[str, Any]] | None = None,
        params: dict[str, Any] | None = None,
        **poll_kwargs,
    ) -> dict[str, Any]:
        """Merge CSV data into a tagged InDesign template."""
        merged_params: dict[str, Any] = {
            "targetDocument": target_document,
            "dataSource": data_source,
            "outputMediaType": output_media_type,
        }
        if params:
            merged_params.update(params)
        body: dict[str, Any] = {"assets": list(assets), "params": merged_params}
        if outputs:
            body["outputs"] = list(outputs)
        return self.run("/v3/merge-data", body, **poll_kwargs)

    def convert_pdf_to_indesign(
        self,
        assets: Iterable[dict[str, Any]],
        target_document: str,
        *,
        output_media_type: str = "application/x-indesign",
        embed_links: bool = False,
        outputs: Iterable[dict[str, Any]] | None = None,
        **poll_kwargs,
    ) -> dict[str, Any]:
        """Convert a PDF to editable INDD or IDML (returns a ZIP of results)."""
        body: dict[str, Any] = {
            "assets": list(assets),
            "params": {
                "targetDocuments": [target_document],
                "outputMediaType": output_media_type,
                "embedLinks": embed_links,
            },
        }
        if outputs:
            body["outputs"] = list(outputs)
        return self.run("/v3/convert-pdf-to-indesign", body, **poll_kwargs)

    def execute_custom_script(
        self,
        script_id: str,
        script_name: str,
        body: dict[str, Any],
        **poll_kwargs,
    ) -> dict[str, Any]:
        """Run a previously registered custom script bundle."""
        path = f"/v3/{urllib.parse.quote(script_id)}/{urllib.parse.quote(script_name)}"
        return self.run(path, body, **poll_kwargs)

    def submit_custom_script(self, zip_path: str) -> Any:
        """Register a custom-script bundle (.zip). Returns the registration info."""
        with open(zip_path, "rb") as fh:
            file_bytes = fh.read()
        boundary = f"----idapi{uuid.uuid4().hex}"
        filename = zip_path.rsplit("/", 1)[-1]
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: application/zip\r\n\r\n"
        ).encode("utf-8")
        body += file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")
        headers = self._headers(content_type=f"multipart/form-data; boundary={boundary}")
        url = f"{self.config.api_base}/v3/scripts"
        _status, _headers, raw = _http("POST", url, headers=headers, data=body)
        return json.loads(raw.decode("utf-8")) if raw else {}
