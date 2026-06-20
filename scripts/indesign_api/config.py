"""Configuration for the Firefly Services InDesign API client.

All values are read from environment variables so that secrets never live in the
repository. Copy ``.env.example`` to ``.env`` and fill it in, or export the
variables in your shell.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

# Adobe IMS server-to-server (OAuth client_credentials) token endpoint.
DEFAULT_IMS_TOKEN_URL = "https://ims-na1.adobelogin.com/ims/token/v3"

# Base URL of the Firefly Services InDesign API.
DEFAULT_API_BASE = "https://indesign.adobe.io"

# Scopes for a Firefly Services credential. The exact set is shown on your
# Adobe Developer Console project credential page; override with ADOBE_SCOPES if
# yours differ.
DEFAULT_SCOPES = "openid,AdobeID,read_organizations,firefly_api,ff_apis"


class ConfigError(RuntimeError):
    """Raised when required configuration is missing."""


@dataclass
class Config:
    """Holds credentials and endpoints for the InDesign API client."""

    client_id: str
    client_secret: str = ""
    scopes: str = DEFAULT_SCOPES
    ims_token_url: str = DEFAULT_IMS_TOKEN_URL
    api_base: str = DEFAULT_API_BASE
    # Optional pre-minted access token. If provided, the client uses it directly
    # and skips the IMS client_credentials exchange (useful for quick tests).
    access_token: str = ""

    @classmethod
    def from_env(cls, env: dict | None = None) -> "Config":
        env = env if env is not None else os.environ
        client_id = env.get("ADOBE_CLIENT_ID", "").strip()
        if not client_id:
            raise ConfigError(
                "ADOBE_CLIENT_ID is required. See "
                "instructions/indesign-automation/README.md for setup."
            )
        access_token = env.get("ADOBE_ACCESS_TOKEN", "").strip()
        client_secret = env.get("ADOBE_CLIENT_SECRET", "").strip()
        if not access_token and not client_secret:
            raise ConfigError(
                "Provide ADOBE_CLIENT_SECRET (to mint a token) or "
                "ADOBE_ACCESS_TOKEN (a pre-minted token)."
            )
        return cls(
            client_id=client_id,
            client_secret=client_secret,
            scopes=env.get("ADOBE_SCOPES", DEFAULT_SCOPES).strip() or DEFAULT_SCOPES,
            ims_token_url=env.get("ADOBE_IMS_TOKEN_URL", DEFAULT_IMS_TOKEN_URL).strip()
            or DEFAULT_IMS_TOKEN_URL,
            api_base=env.get("INDESIGN_API_BASE", DEFAULT_API_BASE).strip()
            or DEFAULT_API_BASE,
            access_token=access_token,
        )
