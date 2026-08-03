import unittest

from file_search_store_utils import build_import_file_request_body


class BuildImportFileRequestBodyTests(unittest.TestCase):
    def test_uses_file_name_field_required_by_api(self):
        self.assertEqual(
            build_import_file_request_body("files/abc123"),
            {"fileName": "files/abc123"},
        )


if __name__ == "__main__":
    unittest.main()
