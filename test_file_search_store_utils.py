import unittest

from file_search_store_utils import (
    build_import_failure_details,
    build_import_file_request_body,
    is_valid_file_search_store_name,
)


class BuildImportFileRequestBodyTests(unittest.TestCase):
    def test_uses_file_name_field_required_by_api(self):
        self.assertEqual(
            build_import_file_request_body("files/abc123"),
            {"fileName": "files/abc123"},
        )


class FileSearchStoreNameTests(unittest.TestCase):
    def test_accepts_api_resource_name(self):
        self.assertTrue(is_valid_file_search_store_name("fileSearchStores/store-123"))

    def test_rejects_display_name(self):
        self.assertFalse(is_valid_file_search_store_name("user_u123"))


class BuildImportFailureDetailsTests(unittest.TestCase):
    def test_includes_status_and_parsed_json(self):
        details = build_import_failure_details(
            actual_store_name="fileSearchStores/store-123",
            uploaded_file_name="files/file-123",
            file_state="ACTIVE",
            status_code=400,
            response_text='{"error":{"message":"Bad Request"}}',
        )

        self.assertEqual(details["status_code"], 400)
        self.assertTrue(details["store_name_valid"])
        self.assertEqual(details["response_json"]["error"]["message"], "Bad Request")

    def test_includes_operation_error_without_json(self):
        details = build_import_failure_details(
            actual_store_name="bad-store-name",
            uploaded_file_name="files/file-123",
            file_state="PROCESSING",
            response_text="plain text error",
            operation_error={"message": "Import failed"},
        )

        self.assertFalse(details["store_name_valid"])
        self.assertEqual(details["response_text"], "plain text error")
        self.assertNotIn("response_json", details)
        self.assertEqual(details["operation_error"]["message"], "Import failed")


if __name__ == "__main__":
    unittest.main()
