# coding=utf-8

from django.db import models
from lib.id_generate import id_generate


class SearchResult(models.Model):

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
    status = models.IntegerField(db_index=True, default=STATUS_NORMAL)
    file_type = models.IntegerField(db_index=True, default=FILE_TYPE_COMMON)



