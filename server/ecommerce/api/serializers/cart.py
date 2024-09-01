from rest_framework import serializers
from utils.exception import CustomException as ce
from rest_framework import serializers
from .product import ProductSerailizer
from common.serializers import DynamicModelSerializer

from ...models import (
    CartItem,
    Product,
    Cart
)



# ! Cart Item Serializer For View a Cart Item
class CartItemSerializer(DynamicModelSerializer):
    product=ProductSerailizer(fields=['title','product_image'])

    # * Custom field for finding total price of an item in cart
    total_product_price=(
        serializers.SerializerMethodField(
            method_name='get_product_price'
            )
        )


    def get_product_price(self,cart_item):
        """
        Custom Method for calculating cart item total
        price based on quantity and price of the product
        """
        return  cart_item.product.price * cart_item.quantity
    

    class Meta:
        model=CartItem
        fields=[
            'id',
            'product',
            'quantity',
            'total_product_price'
        ]




# ! Add Cart Item Serailizer
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    
    class Meta:
        model=CartItem
        fields=['product_id','quantity']


    def validate_product_id(self,value):
        # ? Check if product id exists in Product Model
        if not Product.objects.filter(id=value).exists():
            raise ce(
                message="Product with the given id doesn't exist"
            )
        return value
        

    def save(self, **kwargs):
        """
        Over riding the save method to create 
        a new cart item instance or to update it  
        """
        cart_id=self.context['cart_id']
        user_id=self.context['user_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        
        # ! Check if cart with the cart_id exists or not 
        cart=Cart.objects.filter(id=cart_id,user_id=user_id).exists()
        if not cart:
            raise  ce(
                message='No Such Cart with the given cart_id and User exists'
            )

        # ! Expection is handeled here 
        try:
            # ! if cart item already exists then it just update the quantity
            cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity+=quantity
            cart_item.save()
    
        except Exception as e:
            # ! If there is no such cart item for this product new cart item is created
            cart_item=CartItem.objects.create(cart_id=cart_id,**self.validated_data)

        # ! At last returning the cart_item
        return cart_item

    


# ! Update Cart Item Serializer 
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['id','quantity']



# !Cart Serializer 
class CartSerializer(serializers.ModelSerializer):
    cart_item=CartItemSerializer(
        fields=[
            'id',
            'product',
            'quantity',
            'total_product_price'
        ],
        many=True,
        read_only=True
    )

     # * Custom field for finding total price of cart incuding all cart items
    total_price=serializers.SerializerMethodField()


    def get_total_price(self,cart):
        """
        Calculate Total Price of a particular cart by
        summing up all prices of its items
        """
        total_price=sum(
                cart_item.product.price * cart_item.quantity 
                for cart_item in cart.cart_item.all()
            )

        return total_price


    class Meta:
        model=Cart 
        fields=[
            'id',
            'cart_item',
            'total_price'

        ]

    def create(self, validated_data):
        user_id=self.context['user_id']
        return Cart.objects.create(
            user_id=user_id
        )

