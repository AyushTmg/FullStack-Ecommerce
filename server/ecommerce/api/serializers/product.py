from rest_framework import serializers
from ...models import Product,ProductImage
from common.serializers import DynamicModelSerializer
from common.mixins import UserAssignMixin
from utils.exception import CustomException as ce




    
# !Product Image Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=['id','image']


# !Product Serializer
class ProductSerailizer(UserAssignMixin,DynamicModelSerializer):
    product_image=ProductImageSerializer(many=True,read_only=True)
    is_available=serializers.BooleanField(default=True,read_only=True)
    upload_image=serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )


    class Meta:
        model=Product
        fields=[
            'id',
            'title',
            'description',
            'price',
            'is_available',
            'collection',
            'product_image',
            'upload_image'
        ]

    def validate_upload_image(self,value):
        if len(value)>5:
            raise ce(
                message="You cannot upload more than 5 images."
            )
        return value


    def create(self, validated_data):
        """ 
        Used for Creating a new product and its images
        with the validated data from the user and user_id
        context passed from ProductViewSet
        """
        uploaded_images=validated_data.pop('upload_image')
        product=super().create(validated_data)
        # ! For Creating the Product Images 
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)
        return product



