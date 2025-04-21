from rest_framework import serializers
from .models import *

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'start_date', 'price', 'is_necessity')
        
class MonthlyIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monthly_Income
        fields = ('id', 'income')