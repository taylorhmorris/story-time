import unittest

from ..thscraper import query_all 

class Test(unittest.TestCase):
    def test_query_larousse(self):
        data = query_all('viens')
        self.assertEqual(data['word'], 'venir')
        self.assertEqual(data['ipa'], 'vəniʀ')

if __name__ == '__main__':
    unittest.main()
