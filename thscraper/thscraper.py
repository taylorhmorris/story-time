"""THScraper scrapes several sites to determine information about
French language words, bring the information together into one usable json file
"""
import os
from epitran import Epitran
import logging
from dotenv import load_dotenv

from storyqueries.lexicala import QueryLexicala
from storyqueries.larousse import QueryLarousse
from storyqueries.linguee import QueryLinguee
from storyqueries.pixabay import QueryPixabay
# from thscraper.queries.QueryHuggingFace import QueryHFTTI

def query_all(word):
    """Queries all sites using word parameter"""
    load_dotenv()
    try:
        logger = logging.getLogger("th_scraper")
        logger.setLevel(logging.DEBUG)    
        logger.info("Running Scraper")
                
        logger.debug("Querying Larousse")
        larousse = QueryLarousse().query(word)
        logger.debug("Done Querying Larousse")
        try:
            word = larousse['word']
        except Exception as e:
            logger.error(f"Exception Encountered: {e}")

        logger.debug("Querying Lexicala")
        lexicala_api_key = os.getenv("RAPID_API_KEY", None)
        logger.debug(f"Lexicala API Key =? None: {lexicala_api_key is None}")
        query_lexicala = QueryLexicala(lang='fr', api_key=lexicala_api_key)
        logger.debug("Query Lexicala created")
        lexicala = query_lexicala.query(word)
        logger.debug("Done Querying Lexicala")
        lexicala_definitions = []
        if lexicala and lexicala['results']:
            for result in lexicala['results']:
                if result['language'] == 'fr':
                    for sense in result['senses']:
                        definition = sense.get("definition", None)
                        if definition:
                            lexicala_definitions.append(definition)

        logger.debug("Querying Linguee")
        linguee = QueryLinguee().query(word)
        logger.debug("Done Querying Linguee")

        logger.debug("Querying Pixabay")
        pixabay_api_key = os.getenv("PIXABAY_API_KEY", None)
        pixabay = QueryPixabay(api_key=pixabay_api_key).query(word)
        logger.debug("Done Querying Pixabay")
        images = []
        if pixabay and pixabay['hits']:
            for hit in pixabay['hits']:
                images.append(hit['previewURL'])

        ai_images = []
        # logger.debug("Querying HuggingFaceTextToImage")
        # hf_api_key = os.getenv("HF_API_KEY", None)
        # hf = QueryHFTTI(api_key=hf_api_key).query(word)
        # logger.debug("Done Querying HuggingFaceTextToImage")
        # if hf:
        #     ai_images.append(hf)

        ipa = Epitran('fra-Latn').transliterate(word)
        logger.info(f"ipa found by Epitran == {ipa}")

        data = {
            'word': word,
            'ipa': ipa,
            'definitions': larousse['definitions'] + lexicala_definitions,
            'grammar': larousse['grammar'],
            'examples': linguee['examples'],
            'expressions': larousse['expressions'] + linguee['expressions'],
            'images': images,
            'ai_images': ai_images
        }
        logger.info("Return data")
        logger.debug(f"{data}")
        return data
    except Exception as e:
        logging.error(e)
        return {}

def run():
    """Run demo query to test query_all function"""
    while True:
        s = input("Enter a word: ")
        if s == "exit":
            break
        data = query_all(s)
        print(data)

if __name__ == '__main__':
    run()
