from django.db import models

class Advertisement(models.Model):
    content = models.CharField(max_length=1000)
