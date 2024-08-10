from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from .product import Product


# !Cart Model
class Cart(models.Model):
    time_stamp=models.DateTimeField(auto_now_add=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart')

    def __str__(self) -> str:
        return f"{self.user} cart"


# !CartItem Model
class CartItem(models.Model):
    quantity=models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
        )
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_item')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart_item')


    class Meta:
        unique_together = [['cart', 'product']]