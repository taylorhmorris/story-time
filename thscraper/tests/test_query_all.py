import unittest

from ..thscraper import query_all 

class Test(unittest.TestCase):
    def test_query_larousse(self):
        data = query_all('viens')
        self.assertEqual(data.get('word'), 'venir')
        self.assertEqual(data.get('ipa'), 'vəniʀ')

if __name__ == '__main__':
    unittest.main()
