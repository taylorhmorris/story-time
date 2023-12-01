import unittest

from ..queries.Query import Query

class Test(unittest.TestCase):
    def test_query_respects_params(self):
        query = Query('localhost', 'auth_type', False, 'fakekey', 'new_cache')
        self.assertEqual(query.url, 'localhost')
        self.assertEqual(query.auth, 'auth_type')
        self.assertEqual(query.check_cache, False)
        self.assertEqual(query.api_key, 'fakekey')
        self.assertEqual(query.cache_path, 'new_cache')

    def test_query_has_cache_on_by_default(self):
        query = Query('localhost')
        self.assertEqual(query.check_cache, True)

if __name__ == '__main__':
    unittest.main()
