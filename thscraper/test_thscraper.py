import unittest

from . import thscraper

class Test(unittest.TestCase):
    def test_store_cache_with_newline_word(self):
        q = thscraper.Query.Query('')
        response_data = { 'word': "\n" }
        try:
            res = q.store_in_cache('test', response_data)
        except:
            self.assertEqual(False, True)
        self.assertEqual(res, False)

    def test_store_cache_with_newline_search_string(self):
        q = thscraper.Query.Query('')
        response_data = { 'word': "blob" }
        try:
            res = q.store_in_cache('\n', response_data)
        except:
            self.assertEqual(False, True)
        self.assertEqual(res, False)
    
    def test_retrieve_cache_newline_search_string(self):
        q = thscraper.Query.Query('')
        try:
            res = q.retrieve_cache('\n')
        except:
            self.assertEqual(False, True)
        self.assertEqual(res, False)

if __name__ == '__main__':
    unittest.main()
