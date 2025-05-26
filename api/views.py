from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
# from rest_framework import generics
# from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from .models import *


# Create your views here.

def home(request):
    return HttpResponse("This is the homepage")

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# @method_decorator(ensure_csrf_cookie, name='dispatch')
# class GETCSRFToken(APIView):
#     permission_classes = []
    
#     def get(self, request, *args, **kwargs):
#         csrf_token = get_token(request)
#         response = JsonResponse({'message': 'CSRF cookie set', 'csrfToken': csrf_token})
#         response['X-CSRFToken'] = csrf_token
#         return response
    

# @method_decorator(ensure_csrf_cookie, name='dispatch')
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response(serializer.errors, status=400)


# @method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({'message': 'CSRF cookie set'})
   
    def post(self, request):
        # csrf_token = request.headers.get("X-CSRFToken")
        # print("Received CSRF Token:", csrf_token)
        username = request.data.get('username')
        password = request.data.get('password')
        
        print(f"Username: {username}, Password: {password}")
        
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request, user)

            # Generate new CSRF token (associated with new session)
            # new_csrf_token = get_token(request)

            response = Response({
                'message': 'Login successful',
                'username': user.username,
                'userId': user.id,
                'isAuthenticated': True,
            })
            

            return response
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out'})
    
    
# @ensure_csrf_cookie
# def csrf(request):
#     return JsonResponse({'csrfToken': get_token(request)})


# New auth-check endpoint to verify authentication status
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def auth_check(request):
    """
    Simple endpoint to verify if the user is authenticated.
    Used by the frontend to check if the session is valid.
    """
    return Response({
        'isAuthenticated': request.user.is_authenticated,
        'username': request.user.username,
        'userId': request.user.id
    })
    
# @method_decorator(ensure_csrf_cookie, name='dispatch')
class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:  
            return Project.objects.filter(user=self.request.user)
        else:
            return Project.objects.none()
    
    def list(self, request):
        queryset = self.get_queryset()
        print("User:", request.user)
        print("Is authenticated:", request.user.is_authenticated)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        # csrf_token = request.headers.get("X-CSRFToken")
        # print("Received CSRF Token:", csrf_token)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        # print("X-CSRFToken Header:", request.META.get('HTTP_X_CSRFTOKEN'))
        # print("CSRF Cookie:", request.COOKIES.get('csrftoken'))
        # print("Session Cookie:", request.COOKIES.get('sessionid'))
        if serializer.is_valid(): 
            serializer.save(user=request.user) #sets the user automatically
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = 400)
    
    def retrieve(self, request, pk=None):
        project = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(project)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        project = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.serializer_class(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = 400)
    
    def delete(self, request, pk=None):
        project = get_object_or_404(self.get_queryset(), pk=pk)
        project.delete()
        return Response(status=204)
    
    
    
class MonthlyIncomeViewset(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        user = request.user
        monthly_income, created = Monthly_Income.objects.get_or_create(
            user=user,
            defaults={'income': 0}
        )
        
        income_total = monthly_income.income or 0 
        
        # Get the sum of user projects/payments
        total_payments_price = Project.objects.filter(user=user).aggregate(total=models.Sum('price'))['total'] or 0
        
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
            monthly_income = Monthly_Income.objects.get(user=request.user, pk=pk)  # Use .get() instead of queryset
            serializer = MonthlyIncomeSerializer(monthly_income)
            return Response(serializer.data)
        except Monthly_Income.DoesNotExist:
            return Response({'error': 'Monthly income not found.'}, status=404)

    def update(self, request, pk=None):
        try:
            monthly_income = Monthly_Income.objects.get(user=request.user)  # Use .get() to fetch the specific instance
            serializer = MonthlyIncomeSerializer(monthly_income, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Monthly_Income.DoesNotExist:
            return Response({'error': 'Monthly income not found.'}, status=404)