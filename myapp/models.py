from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    # Created_at = models.DateTimeField(auto_now_add=True) 
    image = models.ImageField(upload_to='products/',null=True, blank= True)
    
    def __str__(self):
        return self.name
    
