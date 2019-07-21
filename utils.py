from urllib.parse import urlparse
from nameparser import HumanName
from difflib import SequenceMatcher
import requests

def parse_url(url):
    o = urlparse(url)
    return {
        'protocol': o.scheme,
        'domain': o.netloc.split(':')[0].replace('www.', ''),
        'port': o.netloc.split(':')[1] if ':' in o.netloc else None,
        'path': o.path,
        'parameters': o.params,
        'query': o.query,
        'anchor': o.fragment
    }


def parse_name(raw_name):
    raw_name = raw_name.strip()
    if len(raw_name.split(' ')) == 1:
        raw_name = raw_name.replace('.', ' ').replace(',', ' ').replace('_', ' ').replace('-', ' ')
    name = HumanName(raw_name)

    virtual_first = name.first if len(name.last) ==0 or str(name.first)[0] > str(name.last)[0] else name.last
    virtual_last = name.last if virtual_first == str(name.first) else name.first

    return {
        'title': name.title,
        'first': virtual_first,
        'middle': name.middle,
        'last': virtual_last
    }


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# TODO to be further developed
def is_abbreviation(a, b):
    long = a if len(a) > len(b) else b
    short = a if long == b else b

    long = long.lower()
    short = short.replace('.', '').lower()

    if len(short) == 1 and short[0] == long[0]:
        return True

    if len(short) == 2 and short[0] == long[0] and -1 < long.find(short[1]) < len(long) - 1:
        return True

    return False


# TODO to be further developed
def contain_name(text, name):
    if text is None:
        return False
    text = text.lower()
    return name['first'].lower() in text or name['last'].lower() in text


def equal(a, b, loose=False):
    if loose:
        return a.lower() in b.lower() or b.lower() in a.lower() or a.lower() == b.lower()
    else:
        return a.lower() == b.lower()


def edit(a, b):
    if type(a) is dict:
        edit = {}
        for k in ['first', 'middle', 'last']:
            if a[k] != b[k]:
                edit[a[k]] = b[k]
        return edit
    return (a, b)


def similar_edit(name_edit, text_edit):
    a = text_edit[0]
    b = text_edit[1]

    new_a = a
    for k, v in name_edit.items():
        new_a = a.replace(k, v)
    return similar(a.lower(), b.lower()) < similar(new_a.lower(), b.lower())

def clean_url(url):
    url = url if url.startswith('http') else "http://" +  url
    return url[:-1] if url[-1] == '/' else url

def get_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    return requests.get(url, headers=headers).content

def remove_prefix(url):
    return url.replace('http://', '').replace('https://','').replace('www.','')

    # if not response or len(etree.HTML(str(response.text)).xpath('//text()')) < 50:
    #     print(f'{url} needs to be rendered by the browser.')
    #     chrome_options = Options()
    #     file_name = "chromedriver"
    #     driver = webdriver.Chrome(f'{os.getcwd()}{os.sep}{file_name}', options=chrome_options)
    #     driver.get(url)
    #     content = bs(str(driver.find_element_by_xpath('/html/body').get_attribute('outerHTML')), 'lxml')
    #     driver.quit()
    #     return str(content)
    # else:
    #     return response.content

# print(contain_name('jinsong-guo.com', {'first': 'jinsong', 'last': 'Guo'}))
#
# print(edit({'first': 'jinsong', 'middle':None, 'last': 'Guo'},
#            {'first':'linsong', 'middle':None, 'last': 'Guo'}))
# print(similar('Guo', 'Gu0'))
