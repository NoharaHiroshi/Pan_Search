# coding=utf-8

from django.db import models
import json


class JSONEncodedDictField(models.TextField):

    def __init__(self, *args, **kwargs):
        self.content = dict()
        super(JSONEncodedDictField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if value is not None:
            self.content = json.dumps(value)
            return self.content
        else:
            return value

    def from_db_value(self, value, expression, connection, context):
        if value is not None and isinstance(value, dict):
            self.content = json.loads(value)
            return self.content
        else:
            return self.content
