# coding=utf-8

import datetime
from django.db import models
from lib.id_generate import id_generate
from lib.base_model import JSONEncodedDictField

class SearchResult(models.Model):
    class Meta:
        db_table = 'main_search_result'

    # 百度网盘、磁力链接
    TYPE_BAIDU, TYPE_MAGNET = range(2)
    # 生效、已失效
    STATUS_NORMAL, STATUS_EXPIRE, STATUS_DELETE = range(3)
    # 文件类型
    FILE_TYPE_COMMON, FILE_TYPE_RAR, FILE_TYPE_FILE, FILE_TYPE_IMG, \
        FILE_TYPE_MUSIC, FILE_TYPE_VIDEO, FILE_TYPE_TXT = range(7)

    id = models.BigIntegerField(primary_key=True, db_index=True, default=id_generate())
    name = models.CharField(max_length=225,  db_index=True)
    type = models.IntegerField(db_index=True, default=TYPE_BAIDU)
    size = models.CharField(max_length=60, default=u'未知')
    author = models.CharField(max_length=60, default=u'未知')
    author_id = models.CharField(max_length=60, default=u'')
    status = models.IntegerField(db_index=True, default=STATUS_NORMAL)
    file_type = models.IntegerField(db_index=True, default=FILE_TYPE_COMMON)
    url = models.CharField(max_length=225)
    create_datetime = models.DateTimeField(default=datetime.datetime.now())
    last_check_datetime = models.DateTimeField(auto_now=True)
    content = JSONEncodedDictField(default=dict())

if __name__ == '__main__':
    s = SearchResult()
    s.content['name'] = 'test'
    print s.content




