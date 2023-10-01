
import json
import logging
from pathlib import Path
from bs4 import BeautifulSoup

import requests


class Query():
    """Query Class to be extended for use with specific sites"""
    def __init__(self, url, auth=None, check_cache=True, api_key=None):
        self.url = url
        self.auth = auth
        self.check_cache = check_cache
        self.api_key = api_key
        self.cache_path = "cache"
        self.service_name = self.__class__.__name__.lstrip('Query').lower()
        if len(self.service_name) == 0:
            self.service_name = "query"
        self.logger = logging.getLogger(f"{self.service_name}")
        self.logger.setLevel(logging.DEBUG)

    def retrieve_cache(self, search_string):
        """Retrieve query data from cache"""
        if len(''.join(e for e in search_string if e.isalnum())) < 1:
            return False
        try:
            with open(f"{self.cache_path}\\{self.service_name}\\{search_string}.json", "r") as json_file:
                data = json.load(json_file)
            return data
        except FileNotFoundError:
            return False
        return False

    def store_in_cache(self, search_string, data):
        """Store query data in cache"""
        Path(f"{self.cache_path}\\{self.service_name}").mkdir(parents=True, exist_ok=True)
        self.logger.debug(f"Storing '{search_string}' in cache")
        if len(''.join(e for e in search_string if e.isalnum())) < 1:
            return False
        try:
            word = data['word']
            if not word or len(''.join(e for e in word if e.isalnum())) < 1:
                return False
        except KeyError as e:
            word = search_string
        try:
            with open(f"{self.cache_path}\\{self.service_name}\\{word}.json", "w") as json_file:
                json.dump(data, json_file)
        except TypeError as e:
            logging.error("Could not serialize data")
            raise e
        return True

    def query(self, search_string):
        """Query the site with search_string"""
        if self.check_cache:
            cached = self.retrieve_cache(search_string)
            if cached:
                self.logger.info(f"Search string ({search_string}) found in cache")
                return self.parse_soup(cached)
        self.logger.info(f"Search string ({search_string}) not found in cache")
        url = self.url.format(search_string=search_string, api_key=self.api_key)
        webpage = requests.get(url)
        soup = BeautifulSoup(webpage.content, features="html.parser")
        results = self.parse_soup(soup)
        self.logger.debug("Results received from soup parser")
        if "word" in results:
            if results["word"] is None:
                results['word'] = search_string
        try:
            self.store_in_cache(results['word'], results)
        except KeyError as e:
            self.logger.error(f"Error storing in cache: results does not have {e} key")
        except Exception as e:
            self.logger.error(f"Error storing in cache: {e}")
        self.logger.debug("Returning query results")    
        return results

    def parse_soup(self, soup):
        """Parse the webpage to find the desired information

        This method should be overridden and designed to properly
        handle data from the given website"""
        raise NotImplementedError
