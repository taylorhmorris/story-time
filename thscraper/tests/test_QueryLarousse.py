import unittest

from ..queries.QueryLarousse import QueryLarousse 

class Test(unittest.TestCase):
    def test_query_larousse(self):
        results = QueryLarousse(True).query('chat')
        self.assertEqual(len(results["definitions"]), 8)
        for definition in results['definitions']:
            self.assertNotRegexpMatches(definition['definition'], '^[1-9]')

    def test_query_larousse_expressions(self):
        results = QueryLarousse(True).query('chat')
        for expression in results['expressions']:
            self.assertTrue(expression['expression'][-1] != ' ')
            self.assertTrue(expression['expression'][-1] != ',')

if __name__ == '__main__':
    unittest.main()
