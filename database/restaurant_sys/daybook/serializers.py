from rest_framework import serializers
from .models import DayBook

class DayBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayBook
        fields = "__all__"