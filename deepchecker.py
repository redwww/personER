import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
import re
import os, sys, io, zipfile
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from lexicalchecker import LexicalChecker
from utils import clean_url, get_content, remove_prefix




class DeepChecker(LexicalChecker):
    ATTRIBUTES = ['link', 'tel', 'email', 'description']  # TODO add more attributes to compare

    def __init__(self, record_a:dict, record_b:dict):
        LexicalChecker.__init__(self, record_a, record_b)
        self._raw_url_A = clean_url(record_a['url'].lower())
        self._raw_url_B = clean_url(record_b['url'].lower())


    def deep_check(self):
        print('-------------------------------\n1) Perform lexical check first:\n-------------------------------\n')
        lexical_result = self.lexical_check()

        if lexical_result is False:
            # rule: deep_equal_records
            # IF (equal_name OR similar_name)
            # AND
            # (
            # linked
            # OR
            # (equal_any_content OR similar_descriptions)
            # )
            # ASSERT deep_equal_records
            print('\n-------------------------------\n2)Now switching to the deep check:\n-------------------------------\n')
            print(f'# The applied rule is:\nrule: deep_equal_records\n'
                  f'IF (equal_name OR similar_name)\n'
                  f'AND ('
                  f'linked '
                  f'OR '
                  f'equal_any_content OR similar_descriptions'
                  f')\n'
                  f'ASSERT deep_equal_records\n')
            result =  (self._equal_name() or self._similar_name()) and self.url_deep_similar() == 1
            print(f'Because:\n{self._summary}\nThe final result is\n{result}.')
            return result

        return True


    def url_deep_similar(self):
         """
         Looks into the two urls, extracts representative information,
         based on which it checks if two urls are the homepages of the same person.

         Note that this function is only called when there is other supportive evidence to
         doubt if these two urls are for the same person.

         For example,
         if you've already detected that the name of two persons are similar,
         then you can call this function to further check the urls,
         otherwise, it is not safe.


         Returns:
             int: the result of duplicate check.
                  1  if two urls seem to be owned by the same person;
                  0  if two urls seem to be owned by different people;
                  -1 if it is hard to decide.
         """
         #  TODO redundant assign
         url_1 = self._raw_url_A
         url_2 = self._raw_url_B

         abstract_1 = self._abstract(url_1)
         if all(len(v) == 0 for v in abstract_1.values()):
             self._summary += f'Deep Check result: Unknown (Hard to perform the deep check ' \
                              f'as there are no extracted useful information from {url_1}.)\n'
             return -1

         abstract_2 = self._abstract(url_2)
         if all(len(v) == 0 for v in abstract_2.values()):
             self._summary += f'Deep Check result: Unknown (Hard to perform the deep check ' \
                              f'as there are no extracted useful information from {url_2}.)\n'
             return -1

         for attribute in self.ATTRIBUTES:
             if attribute == 'link':
                 if remove_prefix(url_1) in [remove_prefix(x) for x in abstract_2[attribute]] \
                         or remove_prefix(url_2) in [remove_prefix(x) for x in abstract_1[attribute]]:
                     self._summary += f'(deep check) links: True\n'
                     return 1
                 continue
             v1 = abstract_1[attribute]
             v2 = abstract_2[attribute]
             if v1 and v2 and len(v1) > 0 and len(v2) > 0:
                 if eval(f'DeepChecker._compare_{attribute}')(v1, v2):
                     self._summary += f'(deep check) similar_{attribute}: True\n'
                     return 1

         self._summary += f'Deep Check result: False (The "{self.ATTRIBUTES}" ' \
                          f'detected in these two urls are not similar at all.\n'
         return 0


    @staticmethod
    def _abstract(url):
        web_content = get_content(url)
        text_nodes = [x for x in etree.HTML(web_content).xpath('//text()[normalize-space(.) != ""]') if '{' not in x]

        abstract_result = {}
        for attribute in DeepChecker.ATTRIBUTES:
            abstract_result[attribute] = eval(f'DeepChecker._detect_{attribute}')(web_content, text_nodes)
        return abstract_result


    # TODO to be further developed.
    @staticmethod
    def _detect_link(web_content=None, text_nodes=None):
        doc = bs(web_content, 'lxml')
        links = [clean_url(a['href']) for a in doc.findAll('a', attrs={'href': re.compile("^http[s]?://")})]
        return links

    # TODO to be further developed.
    @staticmethod
    def _detect_description(web_content=None, text_nodes=None):
        # key_words = ['description']
        bios =[x for x in text_nodes if len(x.split()) > 1]
        return bios

    # TODO to be further developed.
    @staticmethod
    def _detect_email(web_content=None, text_nodes=None):
        emails = [x for x in text_nodes if '@' in x]
        return emails

    # TODO to be further developed.
    @staticmethod
    def _detect_tel(web_content=None, text_nodes=None):
        regex_tel = r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?' \
                    r'(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|' \
                    r'([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*' \
                    r'(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)' \
                    r'?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'
        tels = [x for x in text_nodes if re.findall(regex_tel, x)]
        return tels


    # TODO to be further developed.
    @staticmethod
    def _compare_tel(t1: list, t2: list):
        def normalize_tel(tel):
            return tel.replace(' ', '').replace('-', '')

        normalized_t1 = [normalize_tel(x) for x in t1]
        normalized_t2 = [normalize_tel(x) for x in t2]

        return any(t in normalized_t2 for t in normalized_t1)

    @staticmethod
    def _compare_email(e1: list, e2: list):
        return any(e in e2 for e in e1)

    @staticmethod
    def _compare_description(bio1: list, bio2: list):
        stop_words = set(stopwords.words('english')) # TODO to be automactially switched

        def normalize_bio(bio):
            word_tokens = word_tokenize(bio)
            filtered = [w for w in word_tokens if not w in stop_words and len(w) > 1]
            return filtered

        normalized_bio1 = set(normalize_bio(' '.join(bio1)))
        normalized_bio2 = set(normalize_bio(' '.join(bio2)))

        ratio = len(normalized_bio1.intersection(normalized_bio2)) / min(len(normalized_bio1), len(normalized_bio2))
        return ratio > 0.15



if __name__ == '__main__':
    record_a = {'name': 'Tang Nan', 'url': 'https://www.hbku.edu.qa/en/staff/dr-nan-tang'}
    record_b = {'name': 'Nan Tang', 'url': 'http://da.qcri.org/ntang/index.html'}
    DeepChecker(record_a, record_b).deep_check()

