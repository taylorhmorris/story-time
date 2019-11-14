import json
from pprint import pprint as pp
from bs4 import BeautifulSoup
import requests
from epitran import Epitran

class Query():
    def __init__(self, url, auth=None, check_cache=True, api_key=None):
        self.url = url
        self.auth = auth
        self.check_cache = check_cache
        self.api_key = api_key

    def retrieve_cache(self, search_string):
        try:
            folder = self.__class__.__name__.lstrip('Query').lower()
            with open(f"cache\{folder}\{search_string}.json","r") as json_file:
                data = json.load(json_file)
            return data
        except FileNotFoundError:
            return False
        return False

    def store_in_cache(self, search_string, data):
        folder = self.__class__.__name__.lstrip('Query').lower()
        with open(f"cache\{folder}\{search_string}.json","w") as json_file:
            json.dump(data, json_file)

    def query(self, search_string):
        if self.check_cache:
            cached = self.retrieve_cache(search_string)
            if cached != False:
                return self.parse_soup(cached)
        URL = self.url.format(search_string=search_string, api_key=self.api_key)
        fp = requests.get(URL)
        soup = BeautifulSoup(fp.content, features="html.parser")
        results = self.parse_soup(soup)
        self.store_in_cache(search_string, results)
        return results

    def parse_soup(soup):
        """Placeholder to be overwritten."""
        raise NotImplementedError

class QueryCollins(Query):
    def __init__(self):
        url = "https://www.collinsdictionary.com/dictionary/french-english/{search_string}"
        return super().__init__(url)

    def parse_soup(self, soup):
        pronunciation_span = soup(class_="pron type-")
    
        ipa = pronunciation_span[0].text.rstrip(' \n')
        mp3_url = pronunciation_span[0].a['data-src-mp3']
        return ipa, mp3_url
    
class QueryPixabay(Query):
    def __init__(self, lang='fr'):
        with open('apikeys','r') as file:
            for line in file:
                parts = line.split(':')
                if parts[0] == 'pixabay':
                    api_key = parts[1].strip()
        url = "https://pixabay.com/api/?key={api_key}&q={search_string}&lang={lang}&image_type=photo&safesearch=true"
        self.lang = lang
        return super().__init__(url, api_key=api_key)

    def query(self, search_string):
        if self.check_cache:
            cached = self.retrieve_cache(search_string)
            if cached:
                data = cached
            else:
                data = None
        else:
            data = None
        if data == None:
            URL = self.url.format(search_string=search_string, api_key=self.api_key, lang=self.lang)
            response = requests.get(URL)
            if response.status_code == 200:
                data = json.loads(response.content.decode('utf-8'))
                self.store_in_cache(search_string, data)                
                return data
            else:
                return f"Unknown Error from API (status code: {requests.status_code})"
        return data

class QueryLinguee(Query):
    def __init__(self):
        url = "https://www.linguee.com/english-french/search?source=french&query={search_string}"
        return super().__init__(url)

    def parse_soup(self, soup):
        if type(soup) == dict:
            return soup
        example_spans = soup.findAll("span", {"class": "tag_e"})
        examples = []
        for span in example_spans:
            source = span.find("span", {"class": "tag_s"}).text 
            translation = span.find("span", {"class": "tag_t"}).text
            examples.append({"source": source,
                             "translation": translation})

        try:
            expression_group = soup.findAll(class_="example_lines")[-1].text.split('\n\n\n\n')
        except IndexError:
            expression_group = []
        expressions = []
        for e in expression_group:
            if e != '':
                pairs = e.split(':')[-1].strip('\n').split('—')
                if len(pairs) >= 2:
                    expressions.append({'expression': pairs[0], 'translation': pairs[1].replace('\n','')})
        results = {'examples': examples, 'expressions': expressions}
        return results

class QueryLarousse(Query):
    def __init__(self):
        url = "https://www.larousse.fr/dictionnaires/francais/{search_string}/"
        return super().__init__(url)
    
    def parse_soup(self, soup):
        if type(soup) == dict:
            return soup
        try:
            grammar = soup(class_="CatgramDefinition")[0].contents[0]
        except IndexError:
            grammar = None
        try:
            definitions = soup.findAll("li", {"class": "DivisionDefinition"})
            formatted_definitions = []
            for definition in definitions:
                text = definition.text.split(':')
                formatted_definitions.append({'definition': text[0].strip()})
                try:
                    formatted_definitions[-1]['example'] = text[1].strip()
                except IndexError:
                    pass
            
            locutions = soup.findAll(class_="Locution")
            expressions = []
            for x in locutions:
                express = dict()
                a = None
                b = x.find(class_="AdresseLocution").contents
                try:
                    a = f"({b[0].text.split('.')[0]})"
                    b = b[1].split(',')[0]
                except:
                    b=b[0]
                c = x.find(class_="TexteLocution").text
                if a:
                    express['warning'] = a
                express['expression'] = b
                express['definition'] = c
                expressions.append(express)
                
            difficultes = []
            for d in soup.findAll(class_="DefinitionDifficulte"):
                difficultes.append(d.text.replace(u'\xa0', u' '))
                
            citations = []
            for c in soup.findAll(class_="ListeCitations"):
                c_dict = {}
                try:
                    c_dict["Author"] = c.find(class_="AuteurCitation").text
                except:
                    c_dict["Author"] = ""
                try:
                    c_dict["Info"] = c.find(class_="InfoAuteurCitation").text
                except:
                    c_dict["Info"] = ""
                try:
                    c_dict["Text"] = c.find(class_="TexteCitation").text
                except:
                    c_dict["Text"] = ""
                try:
                    c_dict["Reference"] = c.find(class_="ReferenceCitation").text
                except:
                    c_dict["Reference"] = ""
                citations.append(c_dict)
            
            
            results = {"grammar": grammar, "definitions": formatted_definitions,
                       "expressions": expressions, "warnings": difficultes,
                       "citations": citations}
            return results
        except NameError as e:
            raise e

def query_duckduckgo_images(search_string):
    print("Qing Images")
    URL = "https://duckduckgo.com/?q="+search_string+"&t=h_&iar=images&iax=images&ia=images"
    fp = requests.get(URL)
    soup = BeautifulSoup(fp.content, features="html.parser")
    image_holders = soup.find_all("img")
    print(image_holders)
    images = []
    for image in image_holders:
        images.append(image.img)
    return image_holders
    
def query_google_images(search_string):
    print("Qing Images")
    URL = "https://www.google.fr/search?tbm=isch&source=hp&biw=681&bih=598&ei=m_R2XN6bH6fi0gLN74KACg&q="+search_string+"&gs_l=img.3..0l8j0i10j0.2271.2899..3038...0.0..0.116.592.4j2......2....1..gws-wiz-img.....0..35i39.3w7tEkx3O6Y"
    fp = requests.get(URL)
    soup = BeautifulSoup(fp.content, features="html.parser")
    image_holders = soup.find_all("img")
    images = []
    for image in image_holders:
        print(type(image['src']))
        images.append(image['src'])
    return images

def query_all(word):  
    #ipa, mp3_url = "DUMMY_IPA", "MP3_URL"
    #ipa, mp3_url = query_collins(word) ## collins is blocking scraping
    ipa = Epitran('fra-Latn').transliterate(word)
    #grammar, definitions, examples = "dummy_grammar", ["Def 1", "Def 2"], ["Example 1", "Example 2"]
    larousse = QueryLarousse().query(word)
    linguee = QueryLinguee().query(word)
    
    #images = query_duckduckgo_images(word)
    pixabay = QueryPixabay().query(word)
    images = []
    for hit in pixabay['hits']:
        images.append(hit['previewURL'])
    #images = ["dummy_image_url1", "dummy_image_url2"]
    #images = query_google_images(word)
    
    data = {
        'word': word,
        'ipa': ipa,
        'definitions': larousse['definitions'],
        'grammar': larousse['grammar'],
        'examples': linguee['examples'],
        'expressions': larousse['expressions'] + linguee['expressions'],
        'images': images
    }
    return data

def run():
    data = query_all("lire")
    pp(data)
    return data

if __name__ == '__main__':
    run()
