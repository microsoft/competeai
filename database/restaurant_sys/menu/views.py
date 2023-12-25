from rest_framework import viewsets, response
from django_filters.rest_framework import DjangoFilterBackend
from utils.helpers import convert_to_string_format
from django.http import JsonResponse

from .models import Menu
from .serializers import MenuSerializer

from chef.models import Chef

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = "__all__"
    # TODO: 检查菜品名称是否存在重合？
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        _string = convert_to_string_format(serializer.data)
        return response.Response(_string, content_type='text/plain')
    
def get_score_per_dish(request):
    scores = {}
    # get all chefs from Chef
    chefs = Chef.objects.all()
    # get all chef salaries sum
    chef_salaries = 0
    for chef in chefs:
        chef_salaries += chef.salary
    score1 = min(chef_salaries/5000, 1)

    # get all menus from Menu
    menus = Menu.objects.all()
    # get the price and cost_price of each menu
    for menu in menus:
        score2 = menu.cost_price / (0.8 * menu.price)
        score = 0.5 * score1 + 0.5 * score2
        score = round(score, 2)
        scores[menu.name] = score
    
    return JsonResponse(scores, status=200)
    
