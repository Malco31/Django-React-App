from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_necessity = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    
class Monthly_Income(models.Model):
    income = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Ensure there's only one instance
        if not self.id and Monthly_Income.objects.exists():
            raise Exception("Only one Monthly Income instance is allowed.")
        return super().save(*args, **kwargs)
    
    
    
    