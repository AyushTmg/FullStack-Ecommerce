from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from common.models import BaseModel


#!Product Collection Model
class Collection(BaseModel):
    title=models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.title 
    
