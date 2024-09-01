from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from .product import Product
from common.models import UUIDModel,TimeStampedModel


# !Cart Model
class Cart(UUIDModel):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='cart')

    def __str__(self) -> str:
        return f"{self.user} cart"


# !CartItem Model
class CartItem(UUIDModel,TimeStampedModel):
    quantity=models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
        )
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_item')
    product=models.ForeignKey('ecommerce.Product',on_delete=models.CASCADE,related_name='cart_item')


    class Meta:
        unique_together = [['cart', 'product']]

    def __str__(self) -> str:
        return f"{self.cart} - {self.product.title}"
    