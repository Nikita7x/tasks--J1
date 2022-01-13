from django.db import models


class Images(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    url = models.URLField(null=True, blank=True)
    picture = models.URLField()
    width = models.IntegerField()
    height = models.IntegerField()
    parent_picture = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, )
