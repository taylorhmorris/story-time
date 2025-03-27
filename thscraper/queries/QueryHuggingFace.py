
import requests
import io
from PIL import Image

from pyquaca.query import Query, QueryConfig


class QueryHFTTI(Query):
    """Query Configured to send queries to Hugging Face"""
    def __init__(self, lang='French', api_key=''):
        url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
        self.lang = lang
        config: QueryConfig = {"api_key": api_key}
        super().__init__(url, config=config)

    def query(self, search_string):
        data = None
        if self.check_cache:
            cached = self.retrieve_cache(search_string)
            if cached and cached.get("image"):
                with open(cached["image"], "rb") as image:
                    data = image.read()
        if data is None:
            url = self.url
            headers = {"Authorization": f"Bearer {self.api_key}"}
            llm_prompt = QueryHFLLM(api_key=self.api_key, lang=self.lang).query(search_string)
            self.logger.debug(f"Prompt from QueryHFLLM: {llm_prompt}")
            self.logger.debug("Done Querying HuggingFaceLargeLanguageModel")
            detailed_search_string = llm_prompt
            if detailed_search_string is None:
                detailed_search_string = f"Generate an image to help a user remember the meaning of the {self.lang} word '{search_string}'"
            payload = {"inputs": detailed_search_string}
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                image_bytes = response.content
                data = image_bytes
                image_file  = Image.open(io.BytesIO(image_bytes))
                imagePath: str = self.get_full_cache_path(f"{search_string}.png")
                image_file.save(imagePath)
                self.store_in_cache(search_string, {"word": search_string, "image": imagePath})
                return data
            self.logger.debug(f"Unknown API Error (status code:{response.status_code})")
            return None
        return data


