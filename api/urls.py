from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, LogoutView, ProjectViewset, MonthlyIncomeViewset
from . import views


router = DefaultRouter()
router.register('project', ProjectViewset, basename='project')
router.register('monthly_income', MonthlyIncomeViewset, basename='monthly_income')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('auth-check/', views.auth_check, name='auth-check'),
]


urlpatterns += router.urls


