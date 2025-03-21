
import requests

from thscraper.queries.Query import Query


class QueryHFTTI(Query):
    """Query Configured to send queries to Hugging Face"""
    def __init__(self, lang='French', api_key=''):
        url = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
        self.lang = lang
        super().__init__(url, api_key=api_key)

    def query(self, search_string):
        data = None
        if self.check_cache:
            cached = self.retrieve_cache(search_string)
            if cached:
                data = cached["image"]
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
                self.store_in_cache(search_string, {"word": search_string, "image": image_bytes})
                return data
            self.logger.debug(f"Unknown API Error (status code:{response.status_code})")
            return None
        return data


class QueryHFLLM(Query):
    """Query Configured to send queries to Hugging Face"""
    def __init__(self, lang='French', api_key=''):
        url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        self.lang = lang
        self.parameters = {
            "max_new_tokens": 5000,
            "temperature": 0.01,
            "top_k": 50,
            "top_p": 0.95,
            "return_full_text": False
            }
        self.prompt = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are a helpful and smart assistant. You create helpful prompts for image generation to help a user remember the meaning of the {self.lang} word that is given as a query. If the word is abstract, then you given a clever description. You reply only with the prompt and no preamble.<|eot_id|><|start_header_id|>user<|end_header_id|> Here is the query: ```{search_string}```. Provide precise and concise answer.<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        super().__init__(url, api_key=api_key)

    def query(self, search_string) -> str | None:
        self.logger.debug("Querying HuggingFaceLargeLanguageModel")
        data = None
        if self.check_cache:
            cached = self.retrieve_cache(search_string)
            if cached:
                data = cached
        if data is None:
            url = self.url
            prompt = self.prompt.format(search_string=search_string, self=self)
            payload = {
                "inputs": prompt,
                "parameters": self.parameters
            }
            response = requests.post(url, headers=self.headers, json=payload)
            if response.status_code == 200:
                response_text = response.json()[0]['generated_text'].strip()
                self.store_in_cache(search_string, {"word": search_string, "prompt": response_text})
                return response_text
            self.logger.debug(f"Unknown API Error (status code:{response.status_code})")
            return None
        return data