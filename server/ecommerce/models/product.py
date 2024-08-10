from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from .collection import Collection


#!Product Model
class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price=models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
        )
    is_available=models.BooleanField(default=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='product')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE,related_name='product')


    def __str__(self) -> str:
       return self.title

    
# !Product Image Model
class ProductImage(models.Model):
    image=models.ImageField(upload_to='product/image')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_image')



