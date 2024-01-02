from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    cost_price = models.FloatField()
    description = models.TextField()