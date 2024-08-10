from django.db import models
from django.conf import settings
from .product import Product


# !Product Review Model
class Review(models.Model):
    description=models.TextField()
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='review')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='review')
    time_stamp=models.DateTimeField(auto_now_add=True)


# !Review Reply Model
class Reply(models.Model):
    description=models.TextField()
    review=models.ForeignKey(Review,on_delete=models.CASCADE,related_name='reply')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reply')
    time_stamp=models.DateTimeField(auto_now_add=True)

