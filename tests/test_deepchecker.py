import unittest
from deepchecker import DeepChecker


class DeepCheckerTest(unittest.TestCase):
    def test_deep_check__link_each_other_1(self):
        record_a = {'name': 'Jinsong Guo', 'url': 'https://www.jinsong-guo.com/'}
        record_b = {'name': 'Dr. Jinsong Guo', 'url': 'https://www.cs.ox.ac.uk/people/jinsong.guo'}
        self.assertTrue(DeepChecker(record_a, record_b).deep_check())

    def test_deep_check__link_each_other_2(self):
        record_a = {'name': 'Prof. Georg Gottlob',
                    'url': 'https://www.dbai.tuwien.ac.at/staff/gottlob/'}
        record_b = {'name': 'Professor Georg Gottlob',
                    'url': 'https://www.cs.ox.ac.uk/people/georg.gottlob/'}
        self.assertTrue(DeepChecker(record_a, record_b).deep_check())

    def test_deep_check__link_each_other_3(self):
        record_a = {'name': 'Tim Furche',
                    'url': 'http://furche.net/'}
        record_b = {'name': 'Dr. Tim Furche',
                    'url': 'https://www.cs.ox.ac.uk/people/tim.furche/'}
        self.assertTrue(DeepChecker(record_a, record_b).deep_check())

    def test_deep_check__link_each_other_4(self):
        record_a = {'name': 'Giovanni,Grasso', 'url': 'https://www.cs.ox.ac.uk/people/giovanni.grasso/'}
        record_b = {'name': 'Giovanni Grasso', 'url': 'http://www.giovannigrasso.it/'}
        self.assertTrue(DeepChecker(record_a, record_b).deep_check())

    def test_deep_check__link_each_other_5(self):
        record_a = {'name': 'Dan Olteanu',
                    'url': 'http://www.ox.ac.uk/news-and-events/find-an-expert/professor-dan-olteanu'}
        record_b = {'name': 'dan.olteanu',
                    'url': 'http://www.cs.ox.ac.uk/people/dan.olteanu/'}
        self.assertTrue(DeepChecker(record_a, record_b).deep_check())



    def test_deep_check__content_similar_1(self):
        record_a = {'name': 'saravanan thirumuruganathan',
                    'url': 'https://www.hbku.edu.qa/en/staff/dr-saravanan-thirumuruganathan'}
        record_b = {'name': 'saraanan thirumuruganathn',
                    'url': 'https://saravananthirumuruganathan.appspot.com/'}
        self.assertTrue(DeepChecker(record_a, record_b).deep_check())

    def test_deep_check__content_similar_2(self):
        record_a = {'name': 'Tang Nan', 'url': 'https://www.hbku.edu.qa/en/staff/dr-nan-tang'}
        record_b = {'name': 'Nan Tang', 'url': 'http://da.qcri.org/ntang/index.html'}
        self.assertTrue(DeepChecker(record_a, record_b).deep_check())

    def test_deep_check__content_similar_3(self):
        record_a = {'name': 'emanuel sallinger', 'url': 'https://www.dbai.tuwien.ac.at/staff/sallinger/'}
        record_b = {'name': 'sallinger Emanuel', 'url': 'https://www.cs.ox.ac.uk/people/emanuel.sallinger/'}
        self.assertTrue(DeepChecker(record_a, record_b).deep_check())

    def test_deep_check__content_similar_4(self):
        record_a = {'name': 'thomas lukasiewicz',
                    'url': 'https://www.turing.ac.uk/people/researchers/thomas-lukasiewicz'}
        record_b = {'name': 'thomas.lukasiewiczs',
                    'url': 'http://www.cs.ox.ac.uk/people/thomas.lukasiewicz/'}
        self.assertTrue(DeepChecker(record_a, record_b).deep_check())

