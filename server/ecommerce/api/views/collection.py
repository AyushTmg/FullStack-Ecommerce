
from ...models import Collection,Product
from ..serializers import   CollectionSerializer,ProductSerailizer


from ..paginations import Default
from utils.response import CustomResponse as cr 


from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser,AllowAny

from rest_framework.status import(
    HTTP_201_CREATED,
)




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
    