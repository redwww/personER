from utils import similar, is_abbreviation, contain_name, equal, edit, similar_edit
from utils import parse_url, parse_name


class LexicalChecker:
    def __init__(self, record_a:dict, record_b:dict):
        print(f'Record_A is {record_a}.\nRecord_B is {record_b}.\n')

        self._name_A = parse_name(record_a['name'].lower())
        self._url_A = parse_url(record_a['url'].lower())
        self._name_B = parse_name(record_b['name'].lower())
        self._url_B = parse_url(record_b['url'].lower())
        self._summary = ''

        self._names_are_equal = None
        self._names_are_similar = None
        self._urls_are_equal  = None
        self._informative_urls_are_equal = None
        self._informative_urls_are_similar = None
        self._trusted_urls_are_similar = None


    # rule: equal_record
    # IF equal_name AND equal_url
    # OR equal_name AND equal_informative_url
    # OR equal_name AND similar_informative_url
    # OR similar_name AND equal_url
    # OR similar_name AND equal_informative_url # it can happen as the contains() can be non-exact match
    # OR similar_name AND trusted_similar_url # this is the key to filter fake-duplicates
    # ASSERT equal_record
    def lexical_check(self):
        result = self._equal_name() and self._equal_url() \
               or self._equal_name() and self._equal_informative_url() \
               or self._equal_name() and self._similar_informative_url() \
               or self._similar_name() and self._equal_url() \
               or self._similar_name() and self._equal_informative_url() \
               or self._similar_name() and self._trusted_similar_url()

        rule = 'rule: equal_record\n' \
               'IF equal_name AND equal_url \n' \
               'OR equal_name AND equal_informative_url \n' \
               'OR equal_name AND similar_informative_url \n' \
               'OR similar_name AND equal_url \n' \
               'OR similar_name AND equal_informative_url \n'\
               'OR similar_name AND trusted_similar_url \n'\
               'THEN\n'\
               'ASSERT equal_record'
        print(f'# The applied rule is:\n{rule}\n\nbecause:\n{self._summary} \nthe result is {result}.')

        return result


    def _equal_name(self):
        if self._names_are_equal is not None:
            return self._names_are_equal

        self._names_are_equal = self._name_A == self._name_B
        self._summary += f'equal_name : {self._names_are_equal}.\n'
        # if self._names_are_equal is True:
        #     self._names_are_similar = True
        return self._names_are_equal

    # rule: similar_name
    # IF similar_filed FORALL field in [First_Name, Middle_Name, Last_Name]:
    # # All the titles have been standardized in Step-2, so we don't allow the similar relationship here.
    # ASSERT similar_name
    def _similar_name(self):
        if self._names_are_similar is not None:
            return self._names_are_similar
        self._names_are_similar = self._similar_first_name() and self._similar_last_name() and self._similar_middle_name()
        self._summary += f'similar_name : {self._names_are_similar}\n'
        return self._names_are_similar


    # IF similar(first_name_A, first_name_B)
    # OR
    # is_abbreviation(first_name_A, first_name_B):
    # ASSERT similar_first_name
    def _similar_first_name(self):
        if similar(self._name_A['first'], self._name_B['first']) > 0.65 \
            or is_abbreviation(self._name_A['first'], self._name_B['first']):
            return True
        return False

    # IF similar(middle_name_A, middle_name_B)
    # OR is_abbreviation(middle_name_A, middle_name_B)
    # OR one_is_none(middle_name_A, middle_name_B):
    # ASSERT similar_middle_name
    def _similar_middle_name(self):
        return similar(self._name_A['middle'], self._name_B['middle']) > 0.8 \
                or is_abbreviation(self._name_A['middle'], self._name_B['middle']) \
                or any(a is None for a in [self._name_A['middle'], self._name_B['middle']])


    # rule: similar_last_name
    # IF similar(last_name_A, last_name_B): # No is_abbrevation is allowed for last name
    # ASSERT similar_last_name
    def _similar_last_name(self):
        return similar(self._name_A['last'], self._name_B['last']) > 0.5

    def _equal_url(self):
        if self._urls_are_equal is not None:
            return self._urls_are_equal

        self._urls_are_equal = self._url_A == self._url_B
        self._summary += f'equal_url : {self._urls_are_equal}\n'
        return self._urls_are_equal


    # rule: equal_informative_url:
    # IF equal_informative_domain             # important
    # OR equal_informative_path               # important
    # OR equal_informative_query:             # the last one can be redundant?
    # ASSERT equal_informative_url
    def _equal_informative_url(self):
        if self._informative_urls_are_equal is not None:
            return self._informative_urls_are_equal

        self._informative_urls_are_equal = self._equal_informative_domain() or self._equal_informative_path() or self._equal_informative_query()
        self._summary += f'equal_informative_url : {self._informative_urls_are_equal}\n'
        return self._informative_urls_are_equal


    # Rule: equal_informative_domain
    # IF contain_name(Domain_A, Name_A) AND contain_name(Domain_B, Name_B)
    # AND equal(Domain_Name_A, Domain_Name_B):
    # ASSERT equal_informative_domain
    def _equal_informative_domain(self):
        return contain_name(self._url_A['domain'], self._name_A) and contain_name(self._url_B['domain'], self._name_B) \
               and equal(self._url_A['domain'], self._url_B['domain'])

    # Rule: equal_informative_path
    # IF contain_name(Path_A, Name_A) AND contain_name(Path_B, Name_B)
    # AND equal(Domain_A, Domain_B) AND equal(Path_A, Path_B):
    # ASSERT equal_informative_path
    def _equal_informative_path(self):
        return contain_name(self._url_A['path'], self._name_A) and contain_name(self._url_B['path'], self._name_B) \
               and equal(self._url_A['domain'], self._url_B['domain']) and equal(self._url_A['path'], self._url_B['path'], loose=True)

    # Rule: equal_informative_query
    # IF contain_name(query_A, Name_A) AND contain_name(query_B, Name_B)
    # AND equal(Domain_Name_A, Domain_Name_B) AND equal(Path_A, Path_B) AND equal(query_A, query_B):
    # ASSERT equal_informative_query
    def _equal_informative_query(self):
        return contain_name(self._url_A['query'], self._name_A) and contain_name(self._url_B['query'], self._name_B) \
               and equal(self._url_A['domain'], self._url_B['domain']) and equal(self._url_A['path'], self._url_B['path']) \
               and equal(self._url_A['query'], self._url_B['query'])


    # Rule: similar_informative_url:
    # IF similar_informative_domain OR similar_informative_path OR similar_informative_query:
    # ASSERT similar_informative_url
    def _similar_informative_url(self):
        if self._informative_urls_are_similar is not None:
            return self._informative_urls_are_similar

        self._informative_urls_are_similar = self._similar_informative_domain() \
                                             or self._similar_informative_path() \
                                             or self._similar_informative_query()
        self._summary += f'similar_informative_url : {self._informative_urls_are_similar}\n'
        return self._informative_urls_are_similar

    # Rule: similar_informative_domain
    # IF contain_name(Domain_A, Name_A) AND contain_name(Domain_B, Name_B)
    # AND similar(Domain_A, Domain_B):
    # ASSERT similar_informative_domain
    def _similar_informative_domain(self):
        return contain_name(self._url_A['domain'], self._name_A) and contain_name(self._url_B['domain'], self._name_B) \
               and similar(self._url_A['domain'], self._url_B['domain']) > 0.8

    # IF contain_name(Path_A, Name_A) AND contain_name(Path_B, Name_B)
    # AND similar(Domain_A, Domain_B) AND similar(Path_A, Path_B)
    # ASSERT similar_informative_path
    def _similar_informative_path(self):
        return contain_name(self._url_A['path'], self._name_A) and contain_name(self._url_B['path'], self._name_B) \
               and similar(self._url_A['domain'], self._url_B['domain']) > 0.8 and similar(self._url_A['path'], self._url_B['path']) > 0.7

    # Rule: similar_informative_query
    # IF contain_name(query_A, Name_A) AND contain_name(query_B, Name_B)
    # AND similar(Domain_Name_A, Domain_Name_B) AND similar(Path_A, Path_B) AND similar(query_A, query_B)
    # ASSERT similar_informative_query
    def _similar_informative_query(self):
        return contain_name(self._url_A['query'], self._name_A) and contain_name(self._url_B['query'], self._name_B) \
               and similar(self._url_A['domain'], self._url_B['domain']) > 0.8 and similar(self._url_A['path'], self._url_B['path']) > 0.7 \
               and similar(self._url_A['query'], self._url_B['query']) >0.7


    # Rule: trusted_similar_url
    # IF trusted_similar_informative_domain OR trusted_similar_informative_path OR trusted_similar_informative_query:
    # ASSERT trusted_similar_url
    def _trusted_similar_url(self):
        if self._trusted_urls_are_similar is not None:
            return self._trusted_urls_are_similar

        self._trusted_urls_are_similar = self._trusted_similar_informative_domain() \
                                         or self._trusted_similar_informative_path() \
                                         or self._trusted_similar_informative_path()

        self._summary += f'trusted_similar_url  : {self._trusted_urls_are_similar} \n'
        return self._trusted_urls_are_similar

    # Rule: trusted_similar_informative_domain
    # IF similar_informative_domain
    # AND not_similar(edit(Domain_A, Domain_B), edit(NAME_A, NAME_B)): # Important
    # ASSERT trusted_similar_informative_domain
    def _trusted_similar_informative_domain(self):
        return self._similar_informative_domain() \
               and not similar_edit(text_edit=edit(self._url_A['domain'], self._url_B['domain']), name_edit=edit(self._name_A, self._name_B))


    # Rule: trusted_similar_informative_path
    # IF similar_informative_path
    # AND not_similar(edit(Path_A, Path_B), edit(NAME_A, NAME_B)): # Important
    # ASSERT trusted_similar_informative_path
    def _trusted_similar_informative_path(self):
        return self._equal_informative_path() \
               and not similar_edit(text_edit=edit(self._url_A['path'], self._url_B['path']), name_edit=edit(self._name_A, self._name_B))

    # Rule: trusted_similar_informative_query
    # IF similar_informative_query
    # AND not_similar(edit(query_A, query_B), edit(Name_A,  Name_B)): # Important
    # ASSERT trusted_similar_informative_query
    def _trusted_similar_informative_query(self):
        return self._similar_informative_query() \
               and not similar_edit(text_edit=edit(self._url_A['query'], self._url_B['query']), name_edit=edit(self._name_A, self._name_B))
