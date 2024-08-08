from django.db import models

# Create your models here.

class SecretKey(models.Model):
    name = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
    
