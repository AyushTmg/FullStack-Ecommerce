
from ...models import Cart,CartItem
from ..serializers import CartItemSerializer,AddCartItemSerializer, UpdateCartItemSerializer
from utils.response import CustomResponse as cr



from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from rest_framework.status import(
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
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

    
