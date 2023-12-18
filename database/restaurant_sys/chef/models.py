from django.db import models


class Chef(models.Model):
    name = models.CharField(max_length=30)
    salary = models.IntegerField()