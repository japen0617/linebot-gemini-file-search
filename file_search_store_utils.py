def build_import_file_request_body(file_name: str) -> dict[str, str]:
    """Build the request body for the File Search Store importFile API."""
    return {"fileName": file_name}
