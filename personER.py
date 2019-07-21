import argparse
from deepchecker import DeepChecker
from lexicalchecker import LexicalChecker


parser = argparse.ArgumentParser()

parser.add_argument("-ua", "--url_A", help="url of person_A",
                    type=str, required=True)

parser.add_argument("-ub", "--url_B",  help="url of person_B",
                    type=str, required=True)

parser.add_argument("-na", "--name_A", help="name of person_A",
                    type=str, required=True)

parser.add_argument("-nb", "--name_B", help="name of person_B",
                    type=str, required=True)

parser.add_argument("-deep", "--deep_check",
                    action="store_true", dest='run_deep', default=False,
                    help="run the deep check instead of the default lexical check.")

args = parser.parse_args()

record_A = {'name': args.name_A, 'url': args.url_A}
record_B = {'name': args.name_B, 'url': args.url_B}

if args.run_deep:
    try:
        from nltk.corpus import brown
        brown.words()
    except Exception:
        print(f'The required package is not installed on your machine, now starting the installation.')
        import nltk
        print('Please follow the pop-up window.')
        nltk.download()

    DeepChecker(record_A, record_B).deep_check()
else:
    LexicalChecker(record_A, record_B).lexical_check()





