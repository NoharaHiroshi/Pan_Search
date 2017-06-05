# coding=utf-8

import os
import threading
from lib.get_pan_search_result import SearchResourceHandler


def get_thread_source(search_obj, num):
    share_list = search_obj.share_objects
    count = len(share_list)
    step = count // num if count > num else 1
    s_share_list = list()
    for i in range(0, len(share_list), step):
        if i + step < count:
            s_share_list.append(share_list[i:i+step])
        else:
            s_share_list.append(share_list[i:])
    threads = list()
    num = len(s_share_list) if len(s_share_list) < num else num
    for j in range(num):
        t = threading.Thread(target=search_obj.get_resource, args=(s_share_list[j],))
        threads.append(t)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Pan_Search.settings")
    import django
    django.setup()
    source = SearchResourceHandler()
    get_thread_source(source, 10)
