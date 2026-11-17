import asyncio
import os
import unittest
from unittest.mock import Mock, patch

os.environ.setdefault("ChannelSecret", "test-secret")
os.environ.setdefault("ChannelAccessToken", "test-token")
os.environ.setdefault("GOOGLE_API_KEY", "test-key")

import main


class DocumentListingTests(unittest.TestCase):
    def setUp(self):
        self.cache = patch.dict(main.store_name_cache, {"user_test": "fileSearchStores/test"}, clear=True)
        self.cache.start()

    def tearDown(self):
        self.cache.stop()

    @staticmethod
    def response(payload):
        response = Mock()
        response.json.return_value = payload
        return response

    @patch("requests.get")
    def test_collects_all_pages(self, get):
        get.side_effect = [
            self.response({"documents": [{"name": "first", "displayName": "First"}], "nextPageToken": "next"}),
            self.response({"documents": [{"name": "second", "displayName": "Second"}]}),
        ]
        result = asyncio.run(main.list_documents_in_store("user_test"))
        self.assertEqual([doc["name"] for doc in result], ["first", "second"])
        self.assertEqual(get.call_args_list[1].kwargs["params"]["pageToken"], "next")

    @patch("requests.get")
    def test_empty_store_is_distinct_from_failure(self, get):
        get.return_value = self.response({"documents": []})
        self.assertEqual(asyncio.run(main.list_documents_in_store("user_test")), [])
        get.side_effect = RuntimeError("service unavailable")
        self.assertIsNone(asyncio.run(main.list_documents_in_store("user_test")))

    @patch("requests.get")
    def test_repeated_page_token_is_failure(self, get):
        get.return_value = self.response({"nextPageToken": "repeat"})
        self.assertIsNone(asyncio.run(main.list_documents_in_store("user_test")))


if __name__ == "__main__":
    unittest.main()
