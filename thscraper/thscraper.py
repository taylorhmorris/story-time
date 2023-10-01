"""THScraper scrapes several sites to determine information about
French language words, bring the information together into one usable json file
"""
from epitran import Epitran
import logging
from dotenv import load_dotenv

from thscraper.queries.QueryLarousse import QueryLarousse
from thscraper.queries.QueryLinguee import QueryLinguee
from thscraper.queries.QueryPixabay import QueryPixabay

def query_all(word):
    """Queries all sites using word parameter"""
    #ipa, mp3_url = "DUMMY_IPA", "MP3_URL"
    #ipa, mp3_url = query_collins(word)
    ## collins is blocking scraping
    load_dotenv()
    try:
        logger = logging.getLogger("th_scraper")
        logger.setLevel(logging.DEBUG)    
        logger.info("Running Scraper")
        
        ipa = Epitran('fra-Latn').transliterate(word)
        logger.info(f"ipa found by Epitran == {ipa}")

        logger.debug("Querying Larousse")
        larousse = QueryLarousse().query(word)
        logger.debug("Done Querying Larousse")
        try:
            word = larousse['word']
        except Exception as e:
            logger.error(f"Exception Encountered: {e}")

        # Possibly no longer working. Investigate
        logger.debug("Querying Linguee")
        linguee = QueryLinguee().query(word)
        logger.debug("Done Querying Linguee")

        logger.debug("Querying Pixabay")
        pixabay = QueryPixabay().query(word)
        logger.debug("Done Querying Pixabay")
        images = []
        for hit in pixabay['hits']:
            images.append(hit['previewURL'])

        data = {
            'word': word,
            'ipa': ipa,
            'definitions': larousse['definitions'],
            'grammar': larousse['grammar'],
            'examples': linguee['examples'],
            'expressions': larousse['expressions'] + linguee['expressions'],
            'images': images
        }
        logger.info("Return data")
        return data
    except Exception as e:
        logging.error(e)
        return {}

def run():
    """Run demo query to test query_all function"""
    data = query_all("manger")
    print(data)
    return data

if __name__ == '__main__':
    run()
