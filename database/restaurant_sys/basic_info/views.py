from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.db.models import Max, Avg

from .models import BasicInfo
from .serializers import BasicInfoSerializer

from menu.models import Menu
from comment.models import Comment
from advertisement.models import Advertisement

import json

class BasicInfoViewSet(viewsets.ModelViewSet):
    queryset = BasicInfo.objects.all()
    serializer_class = BasicInfoSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = "__all__"

def Show(request):

    # print(BasicInfo.objects.count())
    try:
        # Get the basic info from the database (assuming there's only one record)
        basic_info = BasicInfo.objects.first()
        name = basic_info.name if basic_info else None

        advertisement = Advertisement.objects.first()
        advertisement = advertisement.content if advertisement else None

        # Get the menu items and exclude the 'price_cost' field
        menu = Menu.objects.values("id", "name", "price", "description")
        # Get the comments from Comment
        customer_score = Comment.objects.aggregate(avg_score=Avg('score'))['avg_score']
        customer_score = customer_score if customer_score else 'NULL'
        comment = Comment.objects.order_by('-id').values("day", "name", "score", "content")[:8]

        data = {
            'name': name,
            'score': customer_score,
            'advertisement': advertisement,
            'menu': list(menu),
            'comment': list(comment),
        }
        return JsonResponse(data, status=200)
    
    except Exception as e:
        # Handle exceptions, e.g., database connection issues
        return JsonResponse({'error': str(e)}, status=500)