# coding=utf-8

import re
import os
from search.models import SearchResult


def validate_file_type(info):
    result = u'.file'
    try:
        if info:
            r = re.compile(u'\.[\w\u4e00-\u9fa5]+$')
            search = r.search(info)
            if search:
                result = search.group()
                _r = re.compile(u'等')
                _search = _r.search(result)
                if _search:
                    result = u'.file(%s)' % result[1:-1]
        return result.upper()
    except Exception as e:
        return e


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Pan_Search.settings")
    import django
    django.setup()
    source_result = SearchResult.objects.all()
    for i in source_result:
        t = validate_file_type(i.name)
        print t


