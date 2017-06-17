# coding=utf-8

import requests
import random


class IPInfo:
    def __init__(self):
        self.api = r'http://api.xicidaili.com/free2016.txt'

    @property
    def ip_pool(self):
        try:
            response = requests.get(self.api)
            ip_pool = response.content.split('\r\n')
            ip_list = [u'http://%s' % ip for ip in ip_pool]
            return ip_list
        except Exception as e:
            print e
            return None


def get_random_ip(pool):
    count = len(pool)
    selected_i = random.randint(0, count)
    ip = pool[selected_i]
    proxy = {
        'http': ip
    }
    return proxy

if __name__ == '__main__':
    ip_obj = IPInfo()
    print ip_obj.ip_pool
