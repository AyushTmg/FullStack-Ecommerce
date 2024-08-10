
from ...models import Review,Reply
from ..serializers import (
    ReviewSerailizer,
    ReplySerializer,
)


from ...permissions import IsObjectUserOrAdminUserElseReadOnly
from utils.response import CustomResponse as cr 
from ..paginations import Default


from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from rest_framework.status import(
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)



#  ! Reply View 
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
    
