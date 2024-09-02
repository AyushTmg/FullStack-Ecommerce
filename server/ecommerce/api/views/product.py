
from ...models import Product,ProductImage,Wishlist
from ..serializers import ProductSerailizer,ProductImageSerializer,EmptySerializer

from ..filters import ProductFilter
from ..paginations import Default
from utils.response import CustomResponse as cr 


from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter,SearchFilter
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from rest_framework.decorators import action

from rest_framework.status import(
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)

from django_filters.rest_framework import DjangoFilterBackend



# !Product ViewSet
class ProductViewSet(ModelViewSet):
    queryset=(
        Product.objects.all()
        .select_related('collection')
        .prefetch_related('product_image')
    )
    
    http_method_names=['get','head','options','post','delete','patch']
    pagination_class=Default

   
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

    def get_serializer_class(self):
        if self.action=='wishlist':
            return EmptySerializer
        return ProductSerailizer


    def get_permissions(self):
        """
        Permission for Product ViewSet
        """
        if self.request.method in permissions.SAFE_METHODS and not self.action:
            return [AllowAny()]
        return [IsAdminUser()]
    

    def get_serializer_context(self):
        """ 
        Passing the user_id as serializer context
        for creating Product object with the logged 
        in user
        """
        if self.request.user.is_authenticated:
            user_id=self.request.user.id
            return {'user_id':user_id}    


    def list(self, request, *args, **kwargs):
        """  
        Overriding the method for custom response
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
        Customized the default retrieve method for showing
        product detail with similar products listing and for
        custom response handling
        """

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        similar_products = (
            Product.objects
            .exclude(id=instance.id)
            .filter(collection=instance.collection)
            .select_related('collection')
            .prefetch_related('product_image')
        )
        related_serializer = self.get_serializer(similar_products, many=True)

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
    

    @action(
        detail=True,
        methods=['GET',"POST",'DELETE'],
        permission_classes=[IsAuthenticated] 
    )
    def wishlist(self,request,pk):
        user_id=request.user.id


        if request.method=='GET':
            if Wishlist.objects.filter(user_id=user_id,product_id=pk).exists():
                return cr.success(
                    data={"on_wishlist":True}
                )
            return cr.success(
                data={"on_wishlist":False}
            )
        
        if request.method=='POST':
            Wishlist.objects.create(user_id=user_id,product_id=pk)
            return cr.success(
                message="Added product on wishlist"
            )
        

        if request.method=='DELETE':
            Wishlist.objects.get(user_id=user_id,product_id=pk).delete()
            return cr.success(
                message="Removed product from the wishlist"
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
    