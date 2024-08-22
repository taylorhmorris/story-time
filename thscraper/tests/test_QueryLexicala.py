import unittest

from ..queries.QueryLexicala import QueryLexicala 

class Test(unittest.TestCase):
    def test_query_lexicala(self):
        data = QueryLexicala(True).query('bonjour')
        self.assertNotEqual(data, None)
        print(data)
        results = data.get('results')
        self.assertNotEqual(results, None)
        self.assertEqual(len(results), 1)
        senses = results[0].get('senses')
        self.assertEqual(len(senses), 1)
        self.assertIsNotNone(senses[0].get('definition'))

if __name__ == '__main__':
    unittest.main()
