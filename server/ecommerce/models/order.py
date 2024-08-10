from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from .product import Product


# !Order Model
class Order(models.Model):
    PENDING="P"
    COMPLETE='C'
    FAILED='F'
    PAYMENT_STATUS=[
        (PENDING,"Pending"),
        (COMPLETE,"Complete"),
        (FAILED,"Failed")
    ]
    time_stamp=models.DateTimeField(auto_now=True)
    payment_status=models.CharField(max_length=1,choices=PAYMENT_STATUS,default=PENDING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='order')


    def __str__(self) -> str:
        return f"{self.user} - {self.payment_status}"
    

    def cancel_order(self):
        """
        Cancel the order and set status to failed
        """
        self.payment_status=self.FAILED
        self.save()
        return "Order is canceled"




# !OrderItem Model
class OrderItem(models.Model):
    quantity=models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
        )
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_item')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_item')


