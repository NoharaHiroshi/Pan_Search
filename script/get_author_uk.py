# coding=utf-8

import os
from lib.get_pan_search_result import get_author_info

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Pan_Search.settings")
    import django
    django.setup()
    get_author_info()
