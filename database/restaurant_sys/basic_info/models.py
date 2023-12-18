from django.db import models

class BasicInfo(models.Model):
    name = models.CharField(max_length=50)
    money = models.IntegerField(default=0)
    rent = models.IntegerField(default=1000)
    status = models.CharField(max_length=50)