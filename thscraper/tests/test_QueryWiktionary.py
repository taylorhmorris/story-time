import os
import unittest

from ..queries.QueryWiktionary import QueryWiktionary, parse_wiktionary_search_page , parse_wiktionary_search_word

class Test(unittest.TestCase):
    def test_parse_wiktionary_search_word(self):
        qw = QueryWiktionary()
        qw.cache_path = os.path.join('.', 'cache', 'test')
        result = qw.query_wiktionary_search_word('chien')
        parsed_json = parse_wiktionary_search_word(result)
        self.assertTrue(parsed_json['totalhits'] > 0)
        self.assertTrue(parsed_json['search'][0]["title"] == 'chien')
        self.assertTrue(parsed_json['search'][0]['pageid'] > 0)

    def test_parse_wiktionary_search_page(self):
        qw = QueryWiktionary()
        qw.cache_path = os.path.join('.', 'cache', 'test')
        result = qw.query_wiktionary_search_page(4939)
        parsed = parse_wiktionary_search_page(result)
        self.assertEqual(len(parsed), 4)
        self.assertEqual(parsed[0]['part_of_speech'], 'Nom commun')
        # print(parsed[0]['text'])
        # self.assertEqual(parsed[0]['soup'], 'Nom commun')

if __name__ == '__main__':
    unittest.main()
