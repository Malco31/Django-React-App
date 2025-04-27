from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .serializers import *
from rest_framework.response import Response
from .models import *

# Create your views here.

def home(request):
    return HttpResponse("This is the homepage")


class ProjectViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def list(self, request):
        queryset = self.queryset.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = 400)
    
    def retrieve(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        serializer = self.serializer_class(project)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        serializer = self.serializer_class(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = 400)
    
    def delete(self, request, pk=None):
        project = self.queryset.get(pk=pk)
        project.delete()
        return Response(status=204)
    
    
    
class MonthlyIncomeViewset(viewsets.ViewSet):
    def list(self, request):
        monthly_income, created = Monthly_Income.objects.get_or_create(
            id=1, defaults={'monthly_income': 0}
        )
        income_total = monthly_income.income or 0 
        
        total_payments_price = Project.objects.aggregate(total=models.Sum('price'))['total'] or 0
        
        remaining_income = income_total - total_payments_price
        
        # Prepare the data
        data = {
            'monthly_income': income_total,  # Send the value
            'remaining_income': remaining_income,
            'total_payments_price': total_payments_price,
        }
        
        return Response(data)  # Return the new data format 
    
    def retrieve(self, request, pk=None):
        try:
            monthly_income = Monthly_Income.objects.get(pk=pk)  # Use .get() instead of queryset
            serializer = MonthlyIncomeSerializer(monthly_income)
            return Response(serializer.data)
        except Monthly_Income.DoesNotExist:
            return Response({'error': 'Monthly income not found.'}, status=404)

    def update(self, request, pk=None):
        try:
            monthly_income = Monthly_Income.objects.get(pk=pk)  # Use .get() to fetch the specific instance
            serializer = MonthlyIncomeSerializer(monthly_income, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Monthly_Income.DoesNotExist:
            return Response({'error': 'Monthly income not found.'}, status=404)