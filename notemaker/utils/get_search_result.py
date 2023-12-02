import base64
import json

import requests
from notemaker.models import SearchResult
from thscraper.thscraper import query_all


def get_search_result(word: str) -> dict | None:
    if word is None or len(word) == 0:
        return None
    try:
        sr = SearchResult.objects.values_list('data', flat=True).get(word=word)
        data = json.decoder.JSONDecoder().decode(sr)
        return data
    except:
        print(f"No Saved Result. Asking thscraper for {word}")
        try:
            data = query_all(word)
            b64images = [base64.b64encode(requests.get(img).content).decode()
                        for img in data['images']]
            data['images'] = b64images
            new_search = SearchResult(word=word)
            new_search.data = json.dumps(data)
            new_search.save()
            return data
        except:
            return None

def set_defaults(data: dict) -> dict:
    try:
        data['definition'] = data['definitions'][0]['definition']
    except (KeyError, IndexError):
        data['definition'] = ''
    try:
        data['expression'] = data['expressions'][0]['expression']
    except (KeyError, IndexError):
        data['expression'] = ''
    try:
        data['expression_meaning'] = data['expressions'][0]['definition']
    except (KeyError, IndexError):
        data['expression_meaning'] = ''
    try:
        data['example'] = data['examples'][0]['source']
    except (KeyError, IndexError):
        data['example'] = ''
    try:
        data['image'] = data['images'][0]
    except (KeyError, IndexError):
        data['image'] = ''
    return data
