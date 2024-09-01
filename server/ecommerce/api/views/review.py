
from ...models import Review
from ..serializers import  ReviewSerailizer
from utils.response import CustomResponse as cr 
from ..paginations import Default
from ...permissions import IsObjectUserOrAdminUserElseReadOnly


from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from rest_framework.status import(
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)



# ! Review ViewSet
class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerailizer
    pagination_class=Default

    # ! Custom Permission Called For Reply ViewSet
    permission_classes=[IsObjectUserOrAdminUserElseReadOnly]


    #* For Ordering reviews   
    filter_backends=[OrderingFilter]


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
    

