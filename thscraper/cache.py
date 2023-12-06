import os

import json
import logging
from pathlib import Path

def store_in_cache(cache_folder: str, cache_filename: str, data):
    """Write data to cache file"""
    logger = logging.getLogger(f"Cache")
    Path(cache_folder).mkdir(parents=True, exist_ok=True)
    logger.debug(f"Updating '{cache_filename}' in cache")
    try:
        cache_file_path = os.path.join(cache_folder, cache_filename)
        with open(cache_file_path, "w") as json_file:
            json.dump(data, json_file)
    except TypeError as e:
        logging.error("Could not serialize data")
        logging.error(f'{e}')
        return False
    return True

def retrieve_from_cache(cache_folder: str, cache_filename: str):
    """Retrieve query data from cache"""
    logger = logging.getLogger(f"Cache")
    try:
        cache_file_path = os.path.join(cache_folder, cache_filename)
        with open(cache_file_path, "r") as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        logger.debug('File Not Found')
    return False
