from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    cost_price = models.IntegerField()
    description = models.TextField()