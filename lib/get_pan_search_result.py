# coding=utf-8

import os
import requests
import random
import json
import time
import datetime
from bs4 import BeautifulSoup as bs
from search.models import SearchResult, AuthorResult
from lib.session import get_session
from lib.id_generate import id_generate
from utils.validate_file_type import validate_file_type


class SearchResultHandler:

    def __init__(self, uk):
        self.uk = uk
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

    @classmethod
    def generate_last_author_id(cls):
        try:
            last_object_id = AuthorResult.objects.order_by('-id')[0].id
        except Exception as e:
            print e
            last_object_id = 0000000000
        return last_object_id

    def store_author(self):
        result = {
            'response': 'ok',
            'info': ''
        }
        try:
            response = requests.get(self.get_user_url, params={'query_uk': self.uk}, headers=self.headers, timeout=30)
        except requests.exceptions.ConnectTimeout:
            result.update({
                'response': 'fail',
                'info': 'response connected timeout'
            })
            return result
        except requests.exceptions.Timeout:
            result.update({
                'response': 'fail',
                'info': 'response connected timeout'
            })
            return result
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
                elif error_no == -55:
                    s = random.randint(0, 360)
                    time.sleep(s)
                    result.update({
                        'response': 'fail',
                        'info': 'errno is -55: too fast, sleep %s s' % s
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


def get_author_info():
    last_uk = SearchResultHandler.generate_last_author_id()
    while True:
        try:
            obj = SearchResultHandler(last_uk)
            result = obj.store_author()
            print 'uk:%s, result:%s' % (last_uk, result)
            last_uk += 1
        except Exception as e:
            print e
            break


class SearchResourceHandler:

    def __init__(self):
        pass

    @property
    def share_objects(self):
        all_objects = AuthorResult.objects.filter(share_count__gt=0)
        if all_objects:
            return all_objects
        else:
            return list()

    @staticmethod
    def get_resource(share_objects):
        result = {
            'response': 'ok',
            'info': ''
        }
        try:
            for obj in share_objects:
                if obj.flag == AuthorResult.FLAG_NEED:
                    SearchResult.objects.filter(author_id=obj.id).delete()
                    with get_session(obj.url) as web_session:
                        soup = bs(web_session.page_source, 'lxml')
                        link_info_list = soup.select('a[class="file-handler b-no-ln dir-handler"]')
                        share_datetime = soup.select('div[class="time-col col"]')[0].get_text()
                        if link_info_list:
                            search_resource_list = list()
                            for link_info in link_info_list:
                                d = link_info.attrs
                                link_url = d.get('href', None)
                                link_title = d.get('title', None)
                                search_resource = SearchResult()
                                search_resource.id = id_generate()
                                search_resource.name = link_title
                                search_resource.url = link_url
                                search_resource.type = SearchResult.TYPE_BAIDU
                                search_resource.file_type = validate_file_type(link_title)
                                search_resource.status = SearchResult.STATUS_NORMAL
                                search_resource.author = obj.name
                                search_resource.author_id = obj.id
                                search_resource.share_datetime = datetime.datetime.strptime(
                                        share_datetime, '%Y-%m-%d %H:%M')
                                search_resource.create_datetime = datetime.datetime.now()
                                search_resource.last_check_datetime = datetime.datetime.now()
                                search_resource_list.append(search_resource)
                                print u'file_name: %s' % link_title
                            SearchResult.objects.bulk_create(search_resource_list)
                            obj.flag = AuthorResult.FLAG_NO_NEED
                            obj.save()
                        else:
                            result = {
                                'response': 'fail',
                                'info': 'link_info_list can not get'
                            }
                else:
                    continue
        except Exception as e:
            result = {
                'response': 'fail',
                'info': '%s' % e
            }
        return result


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Pan_Search.settings")
    import django
    django.setup()
    # get_order_info()
    test = SearchResourceHandler()
    share_obj = test.share_objects
    test.get_resource(share_obj)




