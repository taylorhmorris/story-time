
import json
import requests

from thscraper.queries.Query import Query


class QueryLexicala(Query):
    """Query Configured to send queries to Lexicala"""
    def __init__(self, lang='fr', api_key=''):
        url = "https://lexicala1.p.rapidapi.com/search?source=global&language={lang}&text={search_string}"
        self.lang = lang
        super().__init__(url, api_key=api_key)

    def query(self, search_string):
        self.logger.info(f"Querying Lexicala for {search_string}")
        data = None
        if self.check_cache:
            cached = self.retrieve_cache(search_string)
            if cached:
                data = cached
        if data is None:
            url = self.url.format(search_string=search_string, lang=self.lang)
            response = requests.get(url, headers={'x-rapidapi-key': self.api_key, 'x-rapidapi-host': "lexicala1.p.rapidapi.com"})

            if response.status_code == 200:
                data = json.loads(response.content.decode('utf-8'))
                self.store_in_cache(search_string, data)
                return data
            self.logger.debug(f"Unknown API Error (status code:{response.status_code})")
            return {}
        return data
