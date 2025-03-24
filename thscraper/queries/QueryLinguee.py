
from query_and_cache.query import Query


class QueryLinguee(Query):
    """Query Configured to send queries to Linguee"""
    def __init__(self):
        url = "https://www.linguee.com/english-french/search?source=french&query={search_string}"
        super().__init__(url)

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
