from django.db import models

class DayBook(models.Model):
    income = models.IntegerField(default=0)
    expense = models.IntegerField(default=0)
    num_of_customer = models.IntegerField()
    num_of_chef = models.IntegerField(default=0)
    chef_salary = models.IntegerField(default=0)
    dish_score = models.FloatField(default=0)
    customer_score = models.FloatField(default=0)
    dishes = models.TextField()
    rival_info = models.TextField()