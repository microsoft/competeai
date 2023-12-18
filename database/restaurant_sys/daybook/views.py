from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend

from .models import DayBook
from .serializers import DayBookSerializer

from menu.models import Menu
from chef.models import Chef
from comment.models import Comment
from basic_info.models import BasicInfo
from django.db.models import F, Sum, Avg
from django.http import HttpResponse

import json
  
  
def compute(data):
    profit, expense = 0, 0
    # convert data to json
    try:
        data = json.loads(data)
    except json.JSONDecodeError as e:
        print("JSON Parsing Error:", e)
    
    dishes = data['dishes']  # data: {dish1: count1, dish2: count2, ...}
    
    dishes = json.loads(dishes.replace("'", '"'))

    for key, value in dishes.items():
        # get the price and price cost from Menu according to dish name
        # check the dish name in Menu
        if not Menu.objects.filter(name=key).exists():
            continue
        else:
            price = Menu.objects.get(name=key).price
            cost_price = Menu.objects.get(name=key).cost_price
            # compute the profit
            profit += (price - cost_price) * value
    
    rent = BasicInfo.objects.get(id=1).rent
    chef_salaries = 0
    chefs = Chef.objects.all()
    for chef in chefs:
        chef_salaries += chef.salary   
    expense += chef_salaries / 30
    expense += rent
    
    # update the money in database
    BasicInfo.objects.filter(id=1).update(money=F('money') + profit - expense)
    
    return profit, expense

class DayBookViewSet(viewsets.ModelViewSet):
    queryset = DayBook.objects.all()
    serializer_class = DayBookSerializer
    
    def create(self, request, *args, **kwargs):
        post_data = request
        profit, expense = compute(post_data.body.decode('utf-8'))
        chef_salary = Chef.objects.all().aggregate(Sum('salary'))['salary__sum']
        
        scores = []
        for dish in Menu.objects.all():
            score = 0.5 * (dish.cost_price / dish.price) + 0.5 * (chef_salary / 5000)
            scores.append(score)
        dish_score = sum(scores) / len(scores)
        
        customer_score = Comment.objects.aggregate(avg_score=Avg('score'))['avg_score']
        
        response = super(DayBookViewSet, self).create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            instance = self.queryset.get(pk=response.data['id'])
            instance.profit = profit
            instance.expense = expense
            instance.num_of_chef = Chef.objects.count()
            instance.chef_salary = chef_salary
            instance.dish_score = dish_score
            instance.customer_score = customer_score if customer_score else 0
            instance.save()
        
        return response
    
    
    
    
    
    
    
    
    