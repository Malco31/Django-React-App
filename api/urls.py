from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('project', ProjectViewset, basename='project')
router.register('monthly_income', MonthlyIncomeViewset, basename='monthly_income')

urlpatterns = router.urls

# urlpatterns = [
    
#     path('', home)
# ]