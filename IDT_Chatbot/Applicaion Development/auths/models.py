from django.db import models

# Create your models here.

class VerifyCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.code
