# coding=utf-8

import datetime
import re
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

    id = models.BigIntegerField(primary_key=True, db_index=True, default=id_generate)
    name = models.CharField(max_length=225,  db_index=True)
    type = models.IntegerField(db_index=True, default=TYPE_BAIDU)
    size = models.CharField(max_length=60, default=u'未知')
    author = models.CharField(max_length=60, default=u'未知')
    author_id = models.CharField(max_length=60, default=u'')
    status = models.IntegerField(db_index=True, default=STATUS_NORMAL)
    file_type = models.CharField(max_length=60, db_index=True, default=u'.file')
    url = models.CharField(max_length=225, default='')
    share_datetime = models.DateTimeField()
    create_datetime = models.DateTimeField(default=datetime.datetime.now)
    last_check_datetime = models.DateTimeField(auto_now=True)
    content = JSONEncodedDictField(default=dict())

    @property
    def human_file_type(self):
        h_file_type = re.sub(r'\.', '', self.file_type)
        return h_file_type

    def to_dict(self):
        return {
            u'id': str(self.id),
            u'name': self.name,
            u'type': self.type,
            u'size': self.size,
            u'author': self.author,
            u'author_id': self.author_id,
            u'status': self.status,
            u'file_type': self.human_file_type,
            u'url': self.url,
            u'create_datetime': u'%s' % self.create_datetime,
            u'share_datetime': u'%s' % self.share_datetime,
            u'last_check_datetime': u'%s' % self.last_check_datetime
        }


class AuthorResult(models.Model):
    class Meta:
        db_table = 'main_author_search_result'

    # 生效、注销
    STATUS_NORMAL, STATUS_CLOSE = range(2)

    # 需要抓取、不需要抓取
    FLAG_NEED, FLAG_NO_NEED = range(2)

    id = models.BigIntegerField(primary_key=True, db_index=True)
    url = models.CharField(max_length=225, default=u'')
    name = models.CharField(max_length=225, default=u'匿名')
    status = models.IntegerField(db_index=True, default=STATUS_NORMAL)
    avatar_url = models.CharField(max_length=225, default=u'')
    share_count = models.IntegerField(db_index=True, default=0)
    check_count = models.IntegerField(db_index=True, default=0)
    flag = models.IntegerField(db_index=True, default=FLAG_NEED)
    create_datetime = models.DateTimeField(default=datetime.datetime.now)


if __name__ == '__main__':
    pass



