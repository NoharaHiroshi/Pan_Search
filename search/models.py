from django.db import models

# Create your models here.


class SearchResult(models.Model):

    TYPE_BAIDU, TYPE_MAGNET = range(2)

    STATUS_USED, STATUS_UNUSED = range(2)

    name = models.CharField(max_length=50)
    status = models.IntegerField(default=STATUS_USED)
    type = models.IntegerField()
