
from .models import (
    Collection,
    Product,
    ProductImage,
    Review,
    Reply,
    Cart,
    CartItem,
    Order,
)

from .serializers import (
    CollectionSerializer,
    ProductSerailizer,
    ProductImageSerializer,
    ReviewSerailizer,
    ReplySerializer,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    OrderSerializer,
    CreateOrderSerailzer,
    UpdateOrderSerializer,
    CancelOrderSerializer
)


from .filters import ProductFilter
from .pagination import Default
from .tasks import send_order_cancellation_email_task
from .permissions import IsObjectUserOrAdminUserElseReadOnly
from utils.response.response import CustomResponse as cr 


from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny

from rest_framework.status import(
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)


from django.db.models import Q
from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend






# !Collection ViewSet
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    http_method_names=['get','head','options','post','delete']
    pagination_class=Default 


    def get_permissions(self):
        """
        Permission for Collection ViewSet
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]
    

    def create(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return cr.success(
            data=serializer.data,
            status=HTTP_201_CREATED,
            message="New collection has been created successfully "
        )
    
    
    def retrieve(self, request, *args, **kwargs):
        """ 
        Overriding the default retrieve method to filter
        the product by the collection and  for custom 
        response handling
        """
        
        instance=self.get_object()
        serializer=self.serializer_class(instance)

        # ! Retrives 20 products of the related collections
        products=Product.objects.filter(collection=instance)[:20]
        product_serializer=ProductSerailizer(products,many=True)

        data={
            'collection':serializer.data,
            'products':product_serializer.data
        }

        return cr.success(
            data=data
        )
    

    def destroy(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        self.perform_destroy(instance)

        return cr.success(
            status=HTTP_204_NO_CONTENT,
            message="Collection has been successfully deleted"
        )




# !Product ViewSet
class ProductViewSet(ModelViewSet):
    queryset=(
        Product.objects.all()
        .select_related('collection')
        .prefetch_related('product_image')
    )
    serializer_class=ProductSerailizer
    http_method_names=['get','head','options','post','delete','patch']
    pagination_class=Default
    parser_classes = [MultiPartParser, FormParser]

   
    #* For Searching,Filtering and Ordering products
    filter_backends=[
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter
    ]
    
    # * For Using the Custom filter for Product
    filterset_class=ProductFilter

    #* For Specifying the fields for searching and ordering
    search_fields=['title','description']
    ordering_fields=['price']


    def get_permissions(self):
        """
        Permission for Product ViewSet
        """
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]
    

    def get_serializer_context(self):
        """ 
        Passing the user_id as serializer context
        for creating Product object with the logged 
        in user
        """
        user_id=self.request.user.id
        return {'user_id':user_id}    


    def retrieve(self, request, *args, **kwargs):
        """ 
        Customized the default retrieve method for showing
        product detail with similar products listing and for
        custom response handling
        """

        instance = self.get_object()
        serializer = self.serializer_class(instance)
        
        similar_products = (
            Product.objects
            .exclude(id=instance.id)
            .filter(collection=instance.collection)
            .select_related('collection')
            .prefetch_related('product_image')
        )
        related_serializer = self.serializer_class(similar_products, many=True)

        data = {
            'product_details': serializer.data,
            'similar_products': related_serializer.data
        }

        return cr.success(
            data=data,status=HTTP_200_OK
        )
    

    def create(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return cr.success(
            data=serializer.data,
            status=HTTP_201_CREATED,
            message="New product has been successfully created"
        )
    
    
    def update(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}


        return cr.success(
            data=serializer.data,
            message="Product has been successfully updated"
        )
    

    def destroy(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        self.perform_destroy(instance)

        return cr.success(
            status=HTTP_204_NO_CONTENT,
            message="Product has been successfully deleted"
        )




# !ProductImage ViewSet
class ProductImageViewSet(ModelViewSet):
    serializer_class=  ProductImageSerializer
    http_method_names=['get','head','options']


    # ! Permission for Product Image ViewSet
    permission_classes=[AllowAny]
    

    def get_queryset(self):
        """ 
        Over Riding the queryset for filter 
        the product images by the product id 
        present in the URL  parameter
        """
        product_id=self.kwargs['product_pk']
        return ProductImage.objects.filter(product_id=product_id)
    

    def list(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return cr.success(
            data=serializer.data
        )
    

    def retrieve(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return cr.success(
            data=serializer.data
        )
    



# ! Review ViewSet
class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerailizer
    http_method_names=['get','head','options','post','delete']
    pagination_class=Default

    # ! Custom Permission Called For Reply ViewSet
    permission_classes=[IsObjectUserOrAdminUserElseReadOnly]


    #* For Ordering reviews   
    filter_backends=[OrderingFilter]

    #* For Specifying the fields for ordering
    ordering_fields=['time_stamp']


    def get_queryset(self):
        """ 
        Over Riding the queryset for filtering 
        the review's by the product id 
        present in the URL  parameter
        """
        product_id=self.kwargs['product_pk']

        return (
            Review.objects
            .filter(product_id=product_id)
            .select_related('user')
        )
    

    def get_serializer_context(self):
        """
        Passing the product_id and user_id as 
        serializer context for creating product
        review instance
        """

        product_id=self.kwargs['product_pk']
        user_id=self.request.user.id

        return {
            'product_id':product_id,
            'user_id':user_id
            }
    

    def create(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return cr.success(
            data=serializer.data,
            status=HTTP_201_CREATED,
            message="Your have successfully added review "
        )

    
    def retrieve(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return cr.success(
            data=serializer.data
        )


    def list(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return cr.success(
            data=serializer.data
        )
    

    def destroy(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        self.perform_destroy(instance)

        return cr.success(
            status=HTTP_204_NO_CONTENT,
            message="You have successfully deleted your review"
        )
    




# ! Reply View 
class ReplyViewSet(ModelViewSet):
    http_method_names=['get','head','options','post','delete']
    serializer_class=ReplySerializer
    pagination_class=Default


    #* For Ordering reviews reply 
    filter_backends=[OrderingFilter]

    #* For Specifying the fields for ordering
    ordering_fields=['time_stamp']

    # !Custom Permission Called for Reply ViewSet 
    permission_classes=[IsObjectUserOrAdminUserElseReadOnly]


    def get_queryset(self):
        """ 
        Over Riding the queryset for filtering 
        the review reply's by the review id 
        present in the URL  parameter
        """
        review_id=self.kwargs['review_pk']

        return (
            Reply.objects
            .filter(review_id=review_id)
            .select_related('user')
        )
    

    def get_serializer_context(self):
        """
        Passing the review_id and user_id as 
        serializer context for creating product
        reply instance
        """

        review_id=self.kwargs['review_pk']
        user_id=self.request.user.id

        return {
            'review_id':review_id,
            'user_id':user_id
        }
    

    def list(self, request, *args, **kwargs):
        """
        Over Riding the list  method to add
        corresponding review to it's replies
        """
        
        review=Review.objects.get(id=self.kwargs['review_pk'])
        review_serailizer=ReviewSerailizer(review)
        serializer = self.get_serializer(self.get_queryset(), many=True)

        data={
            'review':review_serailizer.data,
            'replies':serializer.data
        }

        return cr.success(
            data=data
        )
    

    def retrieve(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return cr.success(
            data=serializer.data
        )
    

    def create(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return cr.success(
            data=serializer.data,
            status=HTTP_201_CREATED,
            message="Your have replied to the review "
        )

    

    def destroy(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        self.perform_destroy(instance)

        return cr.success(
            status=HTTP_204_NO_CONTENT,
            message="You have successfully deleted your reply"
        )
    



# ! Cart ViewSet
class CartViewSet(ModelViewSet):
    http_method_names=['get','head','options']
    
    # ! Permissions for Cart ViewSet
    permission_classes=[IsAuthenticated]
    serializer_class=CartSerializer

    

    def get_queryset(self):
        """
        Over Riding the queryset to filter cart
        by authenticated users 
        """
        return (
        Cart.objects.filter(user=self.request.user)
        .prefetch_related(
            'cart_item',
            'cart_item__product',
            'cart_item__product__product_image'
            )
        )
    

    def get_serializer_context(self):
        """
        Passing user_id to serailizer
        """
        user_id=self.request.user.id
        return{'user_id':user_id}
    

    def list(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return cr.success(
            data=serializer.data
        )
    

    def retrieve(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return cr.success(
            data=serializer.data
        )
    
    

    
# ! Cart Item Serializer 
class CartItemViewSet(ModelViewSet):
    http_method_names=['get','head','options','post','delete','put']
    
    # ! Permissions For CartItem ViewSet
    permission_classes=[IsAuthenticated]


    def get_queryset(self):
        """
        Over Riding the queryset for filtering the cart
        item by cart_id presented at URL parameter and 
        user_id also using select_related and prefetch_related
        for optimization
        """
        cart_id=self.kwargs['cart_pk']
        user=self.request.user

        try:
           cart=Cart.objects.get(id=cart_id,user=user)
        except Exception as e:
            raise NotFound('Not found')


        return (
            CartItem.objects
            .filter(cart=cart)
            .select_related('product')
            .prefetch_related('product__product_image')
        )
    

    def get_serializer_class(self):
        """
        Over Rding the get_serializer class for using 
        different serializer for different methods 
        """
        if self.request.method in ['GET','HEAD','OPTIONS']:
            return CartItemSerializer
        
        elif self.request.method=='PUT':
            return UpdateCartItemSerializer
        
        return AddCartItemSerializer
    

    def get_serializer_context(self):
        """
        Passing the cart Id and user_id to
        the serializer 
        """
        cart_id=self.kwargs['cart_pk']
        user_id=self.request.user.id
        return {'cart_id':cart_id,'user_id':user_id}
    

    def retrieve(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return cr.success(
            data=serializer.data
        )
    

    def list(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return cr.success(
            data=serializer.data
        )
    

    def create(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return cr.success(
            data=serializer.data,
            status=HTTP_201_CREATED,
            message="Your product has been successfully added to the cart"
        )
    

    def update(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return cr.success(
            data=serializer.data,
            message="Your cart item has been updated"
        )
    

    def destroy(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        self.perform_destroy(instance)

        return cr.success(
            status=HTTP_204_NO_CONTENT,
            message="Your cart item has been successfully deleted"
        )

    



# ! Order ViewSet
class OrderViewSet(ModelViewSet):
    pagination_class=Default

    #* For Ordering  
    filter_backends=[OrderingFilter]

    #* For Specifying the fields for ordering
    ordering_fields=['time_stamp']

    def get_permissions(self):
        """
        Method for defing the permissions
        """
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    
    def get_queryset(self):
        """
        if request.user is admin or staff user then show
        all orders else only show the order of only those 
        order which belongs to the user
        """
        # !For Admin User 
        if (self.request.user.is_staff or self.request.user.is_superuser):
            return (
                Order.objects.all()
                .select_related('user')
                .prefetch_related(
                    'order_item',
                    'order_item__product',
                    'order_item__product__product_image'
                    )
            )
        
        # ! For a normal User
        return (
            Order.objects.exclude(Q(payment_status="F") | Q(payment_status="C"))
            .filter(user = self.request.user)
            .select_related('user')
            .prefetch_related(
                'order_item',
                'order_item__product',
                'order_item__product__product_image'
                )
            )
        
    
    def get_serializer_class(self):
        """
        For using different serailizer class for 
        differet method and actions 
        """
        if self.action == 'cancel_order': 
            return CancelOrderSerializer 
        if self.request.method =='POST':
            return CreateOrderSerailzer
        elif self.request.method in ['PUT','PATCH']:
            return UpdateOrderSerializer
        return OrderSerializer
    
    
    def get_serializer_context(self):
        """  
        Method which pass user_id as context to
        the serializer
        """
        user_id=self.request.user.id
        return {'user_id':user_id}
    

    def list(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return cr.success(
            data=serializer.data
        )
    

    def retrieve(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return cr.success(
            data=serializer.data
        )
    

    def create(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return cr.success(
            data=serializer.data,
            status=HTTP_201_CREATED,
            message="Youre order has been successfully placed"
        )
    

    def update(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return cr.success(
            data=serializer.data,
            message="The order has has been updated"
        )
    

    def destroy(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        self.perform_destroy(instance)

        return cr.success(
            status=HTTP_204_NO_CONTENT,
            message="Your order has been deleted"
        )

    


    
    
    # ! Custom action for viewing order history
    @action(detail=False, methods=['GET'],permission_classes=[IsAuthenticated])
    def history(self,request):
        """
        For Viewing users Order history
        """
        queryset=(Order.objects
            .filter(user=request.user)
            .select_related('user')
            .prefetch_related(
                'order_item',
                'order_item__product',
                'order_item__product__product_image'
                )
            )
        
        serailizer=OrderSerializer(queryset,many=True)

        return cr.success(
            data=serailizer.data,
        )
    

    # ! Custom action for cancelling a order
    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def cancel_order(self, request, pk):
        """ 
        Custom action for canceling a order
        """
        order = get_object_or_404(Order,id=pk)

        # ! If the method in POST
        if request.method == 'POST':

            if order.payment_status=='F':
                return cr.success(
                    status=HTTP_400_BAD_REQUEST,
                    message="You order has already been cancelled"
                )
            
            elif order.payment_status=='C':
                return cr.error(
                    status=HTTP_403_FORBIDDEN,
                    message="Completed Orders cant be canceled"
                )
            
            try:
                with transaction.atomic():
                    # ! Function Called for canceling a order
                    order.cancel_order()

                    # ! Dictionary Data for User
                    data_for_user={
                        'user':str(order.user),
                        'to_email':order.user.email,
                        'subject':'Your Order Cancellation Mail'
                    }

                    # ! Dictionary Data for Supplier
                    data_for_supplier={
                        'user':str(order.user),
                        'subject':'Users Order Cancellation'
                    }
                    
                    # ! Calling celery task for send when order cancelled
                    send_order_cancellation_email_task.delay(data_for_user,data_for_supplier)
                    
                    return cr.success(
                        "Order has been cancelled successfully.",
                    )
                
            
            except Exception as e:
                return cr.error(
                    message="Failed to cancel the order."
                )






    
