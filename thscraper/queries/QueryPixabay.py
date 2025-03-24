
import json
import requests

from query_and_cache.query import Query, QueryConfig


class QueryPixabay(Query):
    """Query Configured to send queries to Pixabay"""
    def __init__(self, lang='fr', api_key=''):
        url = "https://pixabay.com/api/?key={api_key}&q={search_string}&lang={lang}&image_type=photo&safesearch=true"
        self.lang = lang
        config: QueryConfig = {"api_key": api_key}
        super().__init__(url, config)

    def query(self, search_string):
        data = None
        if self.check_cache:
            cached = self.retrieve_cache(search_string)
            if cached:
                data = cached
        if data is None:
            url = self.url.format(search_string=search_string, api_key=self.api_key, lang=self.lang)
            response = requests.get(url)
            if response.status_code == 200:
                data = json.loads(response.content.decode('utf-8'))
                self.store_in_cache(search_string, data)
                return data
            self.logger.debug(f"Unknown API Error (status code:{response.status_code})")
            return {}
        return data
