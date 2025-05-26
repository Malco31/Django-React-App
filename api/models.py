from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_necessity = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class Monthly_Income(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='income')# OnetoOneField Ensure there's only one instance
    income = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s income: ${self.income}"
    
    
    
    
    