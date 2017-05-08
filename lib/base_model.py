# coding=utf-8

from django.db import models


class JSONEncodedDictField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['dafault'] = dict()
        super(JSONEncodedDictField, self).__init__(*args, **kwargs)