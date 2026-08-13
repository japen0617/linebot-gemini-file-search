from __future__ import annotations

import json
from typing import Any, Optional


def build_import_file_request_body(file_name: str) -> dict[str, str]:
    """Build the request body for the File Search Store importFile API."""
    return {"fileName": file_name}


def is_valid_file_search_store_name(store_name: str) -> bool:
    """Return True when the store name matches the API resource format."""
    return store_name.startswith("fileSearchStores/")


def build_import_context(
    *,
    actual_store_name: str,
    uploaded_file_name: str,
    file_state: str,
) -> dict[str, Any]:
    """Build shared import context for logs."""
    return {
        "actual_store_name": actual_store_name,
        "uploaded_file_name": uploaded_file_name,
        "file_state": file_state,
        "store_name_valid": is_valid_file_search_store_name(actual_store_name),
    }


def build_import_failure_details(
    *,
    actual_store_name: str,
    uploaded_file_name: str,
    file_state: str,
    status_code: Optional[int] = None,
    response_text: Optional[str] = None,
    operation_error: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Build structured diagnostics for importFile failures."""
    details = build_import_context(
        actual_store_name=actual_store_name,
        uploaded_file_name=uploaded_file_name,
        file_state=file_state,
    )

    if status_code is not None:
        details["status_code"] = status_code

    if response_text is not None:
        details["response_text"] = response_text
        try:
            details["response_json"] = json.loads(response_text)
        except json.JSONDecodeError:
            pass

    if operation_error is not None:
        details["operation_error"] = operation_error

    return details
