from .product import ProductSerailizer
from ...signals import order_created
from utils.exception import CustomException as ce
from rest_framework import serializers
from django.db import transaction
from ...models import (
    Cart,
    CartItem,
    Order,
    OrderItem
)



# !Order Item Serializer
class OrderItemSerailizer(serializers.ModelSerializer):
    product=ProductSerailizer(fields=['title','product_image'])
    total_product_price=serializers.SerializerMethodField(method_name='get_total_product_price')

    def  get_total_product_price(self,order_item):
        """
        Custom Method for calculating specific order item total
        price based on quantity and price of the product
        """
        return  order_item.product.price*order_item.quantity
    
    class Meta:
        model=OrderItem
        fields=[
            'id',
            'product',
            'quantity',
            'total_product_price'
        ]




# ! Create Order Serailizer 
class CreateOrderSerailzer(serializers.Serializer):
    
    def validate(self,attrs):
        """
        Method for validating cart id 
        """
        user_id=self.context['user_id']
        cart=Cart.objects.get(user_id=user_id)
        if  not cart:
            raise ce(
                message="Cart with given cart id user_id  doesnt exists"
            )
        
        if CartItem.objects.filter(cart=cart).count() == 0:
            raise ce(
                message='The cart is  completely empty.'
            )
        
        return attrs


    def save(self, **kwargs):
        """
        Method which get the user cart and 
        orders all the cart item in the cart 
        """
        with transaction.atomic():
            user_id=self.context['user_id']
            
            #! Get the cart object from db using validated data
            cart=Cart.objects.get(user_id=user_id)

            # ! Create new order with the user_id
            order=Order.objects.create(user_id=user_id)

            cart_items=CartItem.objects.filter(cart=cart)
            
            order_items=[
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,

                ) for item in cart_items
            ]
            
            # !Creating order items
            OrderItem.objects.bulk_create(order_items)

            # ! Deleteing a cart after the order adn order item is created
            cart.delete()

            # ! Creating another cart for the same user after deleting the ordered cart
            Cart.objects.create(user_id=user_id)

            #  ! Custome signal fired 
            order_created.send_robust(self.__class__,order=order)
            return order 




# ! Order Seriaizer For Viewing Orders 
class  OrderSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField()
    order_item=OrderItemSerailizer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField('get_total_price')


    def get_total_price(self,order):
        """ 
        Custome serailizer field to calculate 
        the total order price including prices 
        of all order items 
        """
        total_price=sum(
            [item.product.price * item.quantity
            for item in order.order_item.all()]
        )
        return total_price

    
    class Meta:
        model=Order
        fields=[
            'id',
            'user',
            'payment_status',
            'order_item',
            'time_stamp',
            'total_price',
        ]




# ! Fo Updating Cart item Serailizer
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta :
        model=Order
        fields=['payment_status']




