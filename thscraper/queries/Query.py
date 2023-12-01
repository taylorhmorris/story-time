import os

import json
import logging
from pathlib import Path
from bs4 import BeautifulSoup

import requests

class Query():
    """Query Class to be extended for use with specific sites"""
    def __init__(self, url, auth=None, check_cache=True, api_key=None, cache_path="cache"):
        self.url = url
        self.auth = auth
        self.check_cache = check_cache
        self.api_key = api_key
        self.cache_path = cache_path
        self.service_name = self.__class__.__name__.lstrip('Query').lower()
        if len(self.service_name) == 0:
            self.service_name = "query"
        self.logger = logging.getLogger(f"{self.service_name}")
        self.logger.setLevel(logging.DEBUG)

    def retrieve_cache(self, search_string):
        """Retrieve query data from cache"""
        if len(''.join(e for e in search_string if e.isalnum())) < 1:
            self.logger.debug('Invalid search string')
            return False
        try:
            cache_file_path = os.path.join(self.cache_path, self.service_name, f"{search_string}.json")
            with open(cache_file_path, "r") as json_file:
                data = json.load(json_file)
            return data
        except FileNotFoundError:
            self.logger.debug('File Not Found')
            return False
        return False

    def store_in_cache(self, search_string, data):
        """Store query data in cache"""
        cache_file_dir = os.path.join(self.cache_path, self.service_name)
        Path(cache_file_dir).mkdir(parents=True, exist_ok=True)
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
            cache_file_path = os.path.join(self.cache_path, self.service_name, f"{word}.json")
            with open(cache_file_path, "w") as json_file:
                json.dump(data, json_file)
        except TypeError as e:
            logging.error("Could not serialize data")
            raise e
        return True

    def query(self, search_string: str):
        """Query the site with search_string"""
        search_string = search_string.lower()
        if self.check_cache:
            cached = self.retrieve_cache(search_string)
            if cached:
                self.logger.info(f"Search string ({search_string}) found in cache")
                return self.parse_soup(cached)
            self.logger.info(f"Search string ({search_string}) not found in cache")
        else:
            self.logger.info('Skipping Cache as requested')
        url = self.url.format(search_string=search_string, api_key=self.api_key)
        webpage = requests.get(url)
        soup = BeautifulSoup(webpage.content, features="html.parser")
        results = self.parse_soup(soup)
        self.logger.debug("Results received from soup parser")
        if "word" not in results or results["word"] is None:
            results['word'] = search_string
        try:
            self.store_in_cache(search_string, results)
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
