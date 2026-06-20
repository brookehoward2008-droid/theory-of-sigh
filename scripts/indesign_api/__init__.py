"""Client for Adobe Firefly Services - InDesign API (https://indesign.adobe.io).

This package wraps the cloud InDesign automation endpoints (data merge, rendition,
custom scripts, document info, PDF<->InDesign conversion) so the book pipeline can
run headless without a local copy of InDesign open.

Quick start:

    from scripts.indesign_api import Config, InDesignClient

    client = InDesignClient(Config.from_env())
    print(client.list_app_versions())

See instructions/indesign-automation/README.md for credential setup.
"""

from .config import Config
from .client import (
    InDesignClient,
    InDesignAPIError,
    JobFailedError,
)

__all__ = [
    "Config",
    "InDesignClient",
    "InDesignAPIError",
    "JobFailedError",
]
