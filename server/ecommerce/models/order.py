from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from common.models import BaseModel


# !Order Model
class Order(BaseModel):
    PENDING = "PENDING"
    SHIPPED = "SHIPPED"
    CANCELED = "CANCELED"
    RETURNED = "RETURNED"
    COMPLETE='COMPLETED'

    ORDER_STATUS_CHOICES = [
        (PENDING, "Pending"),
        (SHIPPED, "Shipped"),
        (CANCELED, "Canceled"),
        (COMPLETE,"Complete"),
        (RETURNED, "Returned"),
    ]

    order_status = models.CharField(
        max_length=100,
        choices=ORDER_STATUS_CHOICES,
        default=PENDING
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='order')
    
    
    def __str__(self) -> str:
        return f"{self.user} - {self.order_status}"
    

    def cancel_order(self):
        """
        Cancel the order and set status to failed
        """
        self.order_status=self.CANCELED
        self.save()
        return "Order is canceled"




# !OrderItem Model
class OrderItem(BaseModel):
    quantity=models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
        )
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_item')
    product=models.ForeignKey('ecommerce.Product',on_delete=models.CASCADE,related_name='order_item')


