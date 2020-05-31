import requests
from bs4 import BeautifulSoup
from googlesearch import search # this is the package 'google'
from size_comparisons.exploration.explore_infoboxes import generate_query
import re
import time
import logging

logger = logging.getLogger(__name__)

HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0'
}

def retrieve_count(query_raw: str):
    query = generate_query(query_raw)

    # Based on https://stackoverflow.com/a/29379918
    r = requests.get(query, allow_redirects=True, headers= HEADERS)

    soup = BeautifulSoup(r.text, 'lxml')
    text = soup.get_text()
    if 'No results found for' in text:
        res_int = 0
    else:
        content = str(soup.find('div',{'id':'result-stats'}))
        print(str(content))
        if str(content) == 'None':
            res_int = 0
        else:
            res = re.search(r'([0-9,]*) result', content)
            res_int = int(res.group(1).strip().replace(',', ''))
    return res_int


def check_abstract(entity: str):
    time.sleep(2)
    count_nothing = retrieve_count(f'"say that {entity} is"')
    time.sleep(2)
    count_a = retrieve_count(f'"say that a {entity} is"')
    time.sleep(2)
    count_an = retrieve_count(f'"say that an {entity} is"')

    abstract =  count_nothing > 10 * count_a and count_nothing > count_an
    return abstract



if __name__ == "__main__":
    # print(check_abstract('love'))
    # print(check_abstract('lemon'))
    # print(check_abstract('freedom'))
    # print(check_abstract('apple'))
    print(check_abstract('sksdkldfnldfnklnldsssssssssssssssssssdfsdfsdfsdfsdffsdfhsdlidslindsilnlinlislslsl'))
