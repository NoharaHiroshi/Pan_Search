# coding=utf-8

import os
from lib.get_pan_search_result import get_author_info
from lib.ip_api import IPInfo, get_random_ip

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Pan_Search.settings")
    import django
    django.setup()
    ip_object = IPInfo()
    get_author_info()
