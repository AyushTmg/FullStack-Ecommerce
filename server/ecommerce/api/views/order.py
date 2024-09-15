
from ...models import Order

from ..serializers import  OrderSerializer,CreateOrderSerailzer,UpdateOrderSerializer,EmptySerializer


from ..paginations import Default
from ...tasks import send_order_cancellation_email_task
from utils.response import CustomResponse as cr 
from common.mixins import UserContextMixin


from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from rest_framework.status import(
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)


from django.db.models import Q
from django.db import transaction
from django.shortcuts import get_object_or_404





# ! Order ViewSet
class OrderViewSet(ModelViewSet,UserContextMixin):
    pagination_class=Default

    #* For Ordering  
    filter_backends=[OrderingFilter]

    #* For Specifying the fields for ordering

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
            Order.objects.exclude(Q(order_status="CANCELED") | Q(order_status="COMPLETED"))
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
            return EmptySerializer 
        if self.request.method =='POST':
            return CreateOrderSerailzer
        elif self.request.method in ['PUT','PATCH']:
            return UpdateOrderSerializer
        return OrderSerializer
    

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

            if order.order_status=='CANCELED':
                return cr.success(
                    status=HTTP_400_BAD_REQUEST,
                    message="You order has already been cancelled"
                )
            
            elif order.order_status=='COMPLETED':
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
