from django.db import models
from django.conf import settings
from common.models import BaseModel


# !Product Review Model
class Review(BaseModel):
    description=models.TextField()
    product=models.ForeignKey('ecommerce.Product',on_delete=models.CASCADE,related_name='review')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='review')


# !Review Reply Model
class Reply(BaseModel):
    description=models.TextField()
    review=models.ForeignKey(Review,on_delete=models.CASCADE,related_name='reply')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reply')

