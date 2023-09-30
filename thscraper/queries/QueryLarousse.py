
import logging

import bs4
from thscraper.queries.Query import Query


class QueryLarousse(Query):
    """Query Configured to send queries to Larousse"""
    def __init__(self):
        url = "https://www.larousse.fr/dictionnaires/francais/{search_string}/"
        super().__init__(url)

    def parse_soup(self, soup):
        if isinstance(soup, dict):
            return soup
        try:
            word = None
            for text_part in soup(class_="AdresseDefinition"):
                for content in text_part.contents:
                    if not isinstance(content, bs4.element.NavigableString):
                        continue
                    if len(''.join(e for e in content if e.isalnum())) < 1:
                        continue
                    word = str(content)
                    break
            if word and "," in word:
                word = word.split(',')[0]
            logging.info(f'Using base form: {word}')
        except IndexError as e:
            word = None
        try:
            grammar = soup(class_="CatgramDefinition")[0].find(text=True, recursive=False)
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
                b = x.find(class_="AdresseLocution").find(text=True, recursive=False)
                try:
                    a = f"({b[0].text.split('.')[0]})"
                    b = b[1].split(',')[0]
                except:
                    b = b[0]
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
            results = {"word": word,
                       "grammar": grammar,
                       "definitions": formatted_definitions,
                       "expressions": expressions,
                       "warnings": difficultes,
                       "citations": citations}
            return results
        except NameError as error:
            logging.error('Name error encountered')
            raise error
