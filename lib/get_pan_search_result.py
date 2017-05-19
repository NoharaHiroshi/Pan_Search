# coding=utf-8

import os
import requests
import random
import json
from search.models import SearchResult, AuthorResult


class SearchResultHandler:

    def __init__(self, uk=None):
        self.uk = uk or self.generate_search_id()
        self.base_url = r'http://yun.baidu.com/share/home'
        self.get_user_url = r'http://yun.baidu.com/pcloud/user/getinfo'
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
        response = requests.get(self.get_user_url, params={'query_uk': self.uk}, headers=self.headers)
        if int(response.status_code) == 200:
            info = json.loads(response.content)
            if info:
                error_no = info.get(u'errno', 1)
                if error_no == 0:
                    user_info_dict = info.get(u'user_info', dict())
                    author_name = user_info_dict.get(u'uname', u'匿名')
                    if author_name == u'匿名':
                        result.update({
                            'response': 'fail',
                            'info': 'can not check hit'
                        })
                    else:
                        try:
                            author_result = AuthorResult()
                            author_result.id = self.uk
                            author_result.name = author_name
                            author_result.avatar_url = user_info_dict.get(u'avatar_url', None)
                            author_result.share_count = user_info_dict.get(u'pubshare_count', 0)
                            author_result.url = ''.join([self.base_url, '?uk=%s' % self.uk])
                            author_result.save()
                        except Exception as e:
                            result.update({
                                'response': 'fail',
                                'info': 'user_id repeat: %s' % e
                            })
                else:
                    result.update({
                        'response': 'fail',
                        'info': 'errno is not 0: %s' % info
                    })
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
