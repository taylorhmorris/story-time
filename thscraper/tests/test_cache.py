import shutil
import unittest
from bs4 import BeautifulSoup

import requests

from thscraper.cache import retrieve_or_request

class Test(unittest.TestCase):
    def tearDown(self) -> None:
        shutil.rmtree('./cache/test')
        return super().tearDown()
    
    def test_retrieve_or_request(self):
        url = 'https://example.com/'
        filepath = './cache/test/test_file_html.html'
        text_response = retrieve_or_request(url, filepath)
        manual_request = requests.get(url)
        self.assertEqual(text_response, manual_request.text)
        soup = BeautifulSoup(text_response, features="html.parser")
        self.assertEqual(soup.title.text, 'Example Domain')

if __name__ == '__main__':
    unittest.main()
