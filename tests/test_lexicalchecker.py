import unittest
from lexicalchecker import LexicalChecker


class LexcicalCheckerTest(unittest.TestCase):
    def test_lexcical_check__name_diff_order(self):
        record_a = {'name': 'Jinsong Guo', 'url': 'http://jinsong-guo.com/en-US'}
        record_b = {'name': 'Guo Jinsong', 'url': 'http://jinsong-guo.com/'}
        self.assertTrue(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexcical_check_name_abbr_1(self):
        record_a = {'name': 'Mr. Janr K. James', 'url': 'http://Janr-james1.com'}
        record_b = {'name': 'Mr. JN King James', 'url': 'http://Janr-james1.com'}
        self.assertTrue(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexcical_check_name_abbr_2(self):
        record_a = {'name': 'Mr. Janr K. James', 'url': 'http://dsadsasa.co.uk/Janr-james1/index'}
        record_b = {'name': 'Mr. JN King James', 'url': 'http://dsadsasa.co.uk/Janr-james1'}
        self.assertTrue(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexical_check__optional_specification_1(self):
        record_a = {'name': 'Jinsong Guo', 'url': 'http://jinsong-guo.com/en-US'}
        record_b = {'name': 'Jinsong Guo', 'url': 'http://jinsong-guo.com/'}
        self.assertTrue(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexical_check__optional_specification_2(self):
        record_a = {'name': 'Jinsong Gu0', 'url': 'http://jinsong-guo.com/en-US'}
        record_b = {'name': 'Jinsong Guo', 'url': 'http://jinsong-guo.com/'}
        self.assertTrue(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexical_check__typos_in_name_1(self):
        record_a = {'name': 'Jinsong Gu0', 'url': 'http://jinsong-guo.com/en-US'}
        record_b = {'name': 'Jinsong Guo', 'url': 'http://jinsong-guo.com/'}
        self.assertTrue(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexical_check__typos_in_name_2(self):
        record_a = {'name': 'Katherine Wong', 'url': 'http://KatherineWong.mi'}
        record_b = {'name': 'Catherine Wong', 'url': 'http://KatherineWong.mi/index'}
        self.assertTrue(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexical_check__typos_in_name_3(self):
        record_a = {'name': 'Mr. Janr JR James', 'url': 'http://Janr-james1.com'}
        record_b = {'name': 'Mr. Jane JR James', 'url': 'http://Janr-james1.com/index.html'}
        self.assertTrue(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexical_check__names_in_diff_convention(self):
        record_a = {'name': 'Dr. Js Guo',
                    'url': 'https://www.jinsong-guo.com/about-me#hyhox5u0imgimage'}
        record_b = {'name': 'Dr. Jinsong Guo', 'url': 'https://www.jinsong-guo.com/about-me'}
        self.assertTrue(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexcical_check__similar_path(self):
        record_a = {'name': 'Yavor Nenov', 'url': 'https://www.cs.ox.ac.uk/isg/people/yavor.nenov/'}
        record_b = {'name': 'Yavor Nenov', 'url': 'https://www.cs.ox.ac.uk/people/yavor.nenov/'}
        self.assertTrue(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexcical_check__similar_name_similar_url(self):
        record_a = {'name': 'Mr. Wade JR Smith', 'url': 'http://wade-smith.com'}
        record_b = {'name': 'Mr. Smith JR Wade', 'url': 'http://www.wade-smith0.com/index.html'}
        self.assertTrue(LexicalChecker(record_a, record_b).lexical_check())

    #  TODO deserves further check
    def test_lexical_check__similar_name_diff_person(self):
        record_a = {'name': 'Mr. Js Guo',
                    'url': 'https://www.linkedin.com/in/jinsong-guo-85766885/?originalSubdomain=uk'}
        record_b = {'name': 'Dr. Jinsong Guo',
                    'url': 'https://www.linkedin.com/in/jinsong-guo-8576289121'}
        self.assertFalse(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexical_check__diff_person_2(self):
        record_a = {'name': 'Richard David',
                    'url': 'https://www.linkedin.com/in/richard-david'}
        record_b = {'name': 'Dr. Wu Guo', 'url': 'https://www.linkedin.com/in/wu-guo-8576289121'}
        self.assertFalse(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexical_check__diff_person_3(self):
        record_a = {'name': 'Tiffany Wong',
                    'url': 'https://tiffany.com'}
        record_b = {'name': 'Dr. Wu Guo', 'url': 'https://www.linkedin.com/in/wu-guo-8576289121'}
        self.assertFalse(LexicalChecker(record_a, record_b).lexical_check())


    #
    # Tough cases
    #


    def test_lexical_check__similar_name_but_diff_person_1(self):
        record_a = {'name': 'linsong zhuo', 'url': 'http://linsong-zhuo.com'}
        record_b = {'name': 'Jinsong Guo', 'url': 'http://jinsong-guo.com'}
        self.assertFalse(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexical_check__similar_name_but_diff_person_2(self):
        record_a = {'name': 'Katherine Wong', 'url': 'http://KatherineWong.mi'}
        record_b = {'name': 'Catherine Wang', 'url': 'http://CatherineWang.mi/index'}
        self.assertFalse(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexical_check__similar_name_but_diff_person_3(self):
        record_a = {'name': 'Mr. Wade JR James', 'url': 'http://wade-james1.com'}
        record_b = {'name': 'Mr. Jane JR Wade', 'url': 'http://www.wade-jane.com/index.html'}
        self.assertFalse(LexicalChecker(record_a, record_b).lexical_check())

    def test_lexical_check__similar_name_but_diff_person_4(self):
        record_a = {'name': 'Mr. Janr Jeayer James', 'url': 'http://Janr-james1.com'}
        record_b = {'name': 'Mr. Jane JR James', 'url': 'http://Jane-james1.com/index.html'}
        self.assertFalse(LexicalChecker(record_a, record_b).lexical_check())