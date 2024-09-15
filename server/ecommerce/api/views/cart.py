
from ...models import Cart
from ..serializers import CartSerializer

from utils.response import CustomResponse as cr 
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated





# ! Cart ViewSet
class CartViewSet(ReadOnlyModelViewSet):    
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
    
    