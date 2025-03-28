import unittest

from pyquaca import Query, JSONCache

class Test(unittest.TestCase):
    def test_store_cache_with_newline_word(self):
        q = Query('')
        q.cache = JSONCache('cache')
        response_data = { 'word': "\n" }
        try:
            res = q.cache.store('test', response_data)
        except:
            self.assertEqual(False, True)
        self.assertEqual(res, True)

    @unittest.skip('Test is environment dependent')
    def test_store_cache_with_newline_search_string(self):
        q = Query('')
        response_data = 'blahblah'
        try:
            res = q.cache.store('\n', response_data)
        except:
            self.assertEqual(False, True)
        self.assertEqual(res, True)
    
    def test_retrieve_cache_newline_search_string(self):
        q = Query('')
        try:
            res = q.cache.retrieve('\n')
        except:
            self.assertEqual(False, True)
        self.assertEqual(res, None)

if __name__ == '__main__':
    unittest.main()
