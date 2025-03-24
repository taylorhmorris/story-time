import os
import shutil
import unittest
from bs4 import BeautifulSoup

import requests

from query_and_cache.cache import retrieve_or_request

class Test(unittest.TestCase):
    def tearDown(self) -> None:
        path = os.path.join('.', 'cache', 'test', 'html')
        shutil.rmtree(path)
        return super().tearDown()
    
    def test_retrieve_or_request(self):
        url = 'https://example.com/'
        filepath = os.path.join('.', 'cache', 'test', 'html', 'test_file_html.html')
        text_response = retrieve_or_request(url, filepath)
        manual_request = requests.get(url)
        self.assertEqual(text_response, manual_request.text)
        soup = BeautifulSoup(text_response, features="html.parser")
        if not soup.title:
            self.fail('No title tag found')
        self.assertEqual(soup.title.text, 'Example Domain')

if __name__ == '__main__':
    unittest.main()
