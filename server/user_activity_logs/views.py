from authentication.models import User 
from .serializers import UserActivitySerializer
from utils.response import CustomResponse as cr


from rest_framework.decorators import action
from rest_framework.status  import HTTP_204_NO_CONTENT
from common.views import ListCreateRetrieveUpdateViewSet
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.permissions import IsAdminUser,IsAuthenticated


from django_filters.rest_framework import DjangoFilterBackend




# ! User Activity ViewSet 
class UserActvityViewSet(ListCreateRetrieveUpdateViewSet):
    permission_classes=[IsAdminUser]

    filter_backends=[
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    search_fields=['username','email','id']
    ordering_fields=['username','id']
        
    # ! Serailizer Class 
    serializer_class=UserActivitySerializer
    


    def get_queryset(self):
        """
        Method to over ride the queryset to return user activity
        of all the user in the database for admin user 
        """

        return User.objects.all().prefetch_related(
                'order',
                'order__order_item',
                'order__order_item__product',
                'order__order_item__product__product_image',
                'review'
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
    

    def retrieve(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return cr.success(
            data=serializer.data
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
             message="Data Updated Successfully"
            )
    

    def destroy(self, request, *args, **kwargs):
        """
        Over-riding the method for custom response handling
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return cr.success(
             message="User account has been successfully deleted ",
             status=HTTP_204_NO_CONTENT
             )
       



    # !Custom Action for normal user's 
    @action(detail = False,methods=['GET','PUT'], permission_classes=[IsAuthenticated])
    def me(self,request):
        """
        Adding custom me action in the viewset to show the user activity
        of the logged in normal users 
        """

        user=self.request.user
        # ! Viewing the normal user activty logs 
        if self.request.method=='GET':
                user=User.objects.filter(id=user.id).prefetch_related(
                    'order',
                    'order__order_item',
                    'order__order_item__product',
                    'order__order_item__product__product_image',
                    'review'
                    )
                serializer=self.serializer_class(user,many=True)
                return cr.success(
                     data=serializer.data
                )
        

        # ! Taking the data from the request and updating the noraml user instance
        if self.request.method=='PUT':
            serializer=self.serializer_class(user,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return cr.success(
                 data=serializer.data,
                 message="Your data has been successfully updated"
                )
        


    

    
        

    
       