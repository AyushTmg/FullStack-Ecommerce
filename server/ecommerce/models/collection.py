from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


#!Product Collection Model
class Collection(models.Model):
    title=models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.title 
    
