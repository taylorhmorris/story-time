import unittest

from unittest.mock import patch

from ..thscraper import query_all 

class Test(unittest.TestCase):
    @patch('thscraper.queries.QueryHuggingFace.requests.post')
    def test_query_larousse(self, mock_post):
        data = query_all('viens')
        self.assertEqual(data.get('word'), 'venir')
        self.assertEqual(data.get('ipa'), 'vəniʀ')

if __name__ == '__main__':
    unittest.main()
