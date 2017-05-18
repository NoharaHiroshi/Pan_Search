# coding=utf-8

import os
import requests
import random
from bs4 import BeautifulSoup as bs
from search.models import SearchResult, AuthorResult


class SearchResultHandler:

    def __init__(self):
        self.uk = self.generate_search_id()
        self.base_url = r'http://yun.baidu.com/share/home'
        self.params = {'uk': self.uk}
        self.headers = {'content-type': 'application/json',
                        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    @staticmethod
    def generate_search_id():
        randint_list = list()
        randint_list.append(str(random.randint(1, 3)))
        for i in range(0, 9):
            randint_list.append(str(random.randint(0, 9)))
        uk = ''.join(randint_list)
        return uk

    def store_author(self):
        result = {
            'response': 'ok',
            'info': ''
        }
        response = requests.get(self.base_url, params=self.params, headers=self.headers)
        if int(response.status_code) == 200:
            soup = bs(response.content, 'lxml')
            info = soup.select('span[class="homepagelink"]')
            count_info = soup.select('em[id="sharecnt_cnt"]')
            if info:
                author_name = info[0].get_text()
                if author_name == u'匿名':
                    result.update({
                        'response': 'fail',
                        'info': 'can not check hit'
                    })
                else:
                    if count_info:
                        share_count = int(count_info[0].get_text())
                    else:
                        share_count = 0
                    author_result = AuthorResult()
                    author_result.id = self.uk
                    author_result.url = response.url
                    author_result.share_count = share_count
                    author_result.save()
            else:
                result.update({
                    'response': 'fail',
                    'info': 'can not get info'
                })
        else:
            result.update({
                'response': 'fail',
                'info': 'response status_code is not 200'
            })
        return result


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Pan_Search.settings")
    import django
    django.setup()
    for i in range(10000):
        test = SearchResultHandler()
        print test.store_author()
