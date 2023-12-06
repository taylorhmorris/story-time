import os

import json
import logging
from pathlib import Path

def store_in_cache(file_path: str, data):
    """Write data to cache file"""
    logger = logging.getLogger(f"Cache")
    cache_folder = os.path.dirname(file_path)
    Path(cache_folder).mkdir(parents=True, exist_ok=True)
    logger.debug(f"Updating '{file_path}' in cache")
    try:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)
    except TypeError as e:
        logging.error("Could not serialize data")
        logging.error(f'{e}')
        return False
    return True

def retrieve_from_cache(file_path: str):
    """Retrieve query data from cache"""
    logger = logging.getLogger(f"Cache")
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        logger.debug('File Not Found')
    return False
