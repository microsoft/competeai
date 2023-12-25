from rest_framework import viewsets, response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.db.models import Max

from .models import Comment
from .serializers import CommentSerializer

from utils.helpers import convert_to_string_format

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = "__all__"
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        _string = convert_to_string_format(serializer.data)
        return response.Response(_string, content_type='text/plain')
    
def get_last_comment(self):
    # Determine the maximum value of the 'day' field
    max_day = Comment.objects.aggregate(Max('day'))['day__max']
    # Filter based on this maximum value and get the 'name' and 'content' fields
    comments = Comment.objects.filter(day=max_day).values("name", "content")
    comments = list(comments)
    return JsonResponse(comments, status=200, safe=False)