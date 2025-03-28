
import json

from bs4 import BeautifulSoup
from pyquaca.query import Query

def parse_wiktionary_search_word(json):
    results = dict()
    try:
        results['totalhits'] = json['query']['searchinfo']['totalhits']
    except:
        results['totalhits'] = 0
    try:
        results['search'] = json['query']['search']
    except:
        results['search'] = dict()
    return results

def parse_wiktionary_search_page(json):
    soup = BeautifulSoup(json['parse']['text'], features='html.parser')
    results = []
    for definition in soup.findAll(class_="titredef"):
        result = dict()
        result['part_of_speech'] = definition.text
        result['soup'] = definition.find_next('ol')
        all_text = 'text: '
        for child in definition.find_next('ol').find_next('li').descendants:
            if child.name == 'ul':
                # print('BREAKING')
                break
            if child.text:
                all_text += child.text + '\n'
        # all_text = definition.find_next('ol').descendants
        result['text'] = all_text
        results.append(result)
    return results

class QueryWiktionary(Query):
    """Query Configured to send queries to Wiktionary"""
    def __init__(self, lang="fr"):
        self.lang = lang
        url = "https://{lang}.wiktionary.org/w/api.php?action=query&format=json&formatversion=2&list=search&srsearch={search_string}"
        super().__init__(url)

    def query_wiktionary_search_word(self, word: str):
        url = f"https://{self.lang}.wiktionary.org/w/api.php?action=query&format=json&formatversion=2&list=search&srsearch={word}"
        # path = self.get_full_cache_path(f"{word}.search.json")
        # result = retrieve_or_request(url, path)
        # return json.loads(result)
    
    def query_wiktionary_search_page(self, page: int):
        url = f"https://{self.lang}.wiktionary.org/w/api.php?action=parse&format=json&formatversion=2&pageid={page}"
        # path = self.get_full_cache_path(f"{page}.page.json")
        # result = retrieve_or_request(url, path)
        # return json.loads(result)

    def parse_soup(self, soup):
        if isinstance(soup, dict):
            return soup
        example_spans = soup.findAll("span", {"class": "tag_e"})
        examples = []
        for span in example_spans:
            source = span.find("span", {"class": "tag_s"}).text
            translation = span.find("span", {"class": "tag_t"}).text
            examples.append({"source": source,
                             "translation": translation})

        try:
            expression_group = soup.findAll(class_="example_lines")[-1].text.split('\n\n\n\n')
        except IndexError:
            expression_group = []
        expressions = []
        for expression in expression_group:
            if expression != '':
                pairs = expression.split(':')[-1].strip('\n').split('—')
                if len(pairs) >= 2:
                    expressions.append({'expression': pairs[0],
                                        'translation':
                                            pairs[1].replace('\n', '')})
        results = {'examples': examples, 'expressions': expressions}
        return results
