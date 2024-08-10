from rest_framework import serializers
from ...models import Product,ProductImage
from common.serializers import DynamicModelSerializer




    
# !Product Image Serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields=['id','image']


        
# !Product Serializer
class ProductSerailizer(DynamicModelSerializer):
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


    def create(self, validated_data):
        """ 
        Used for Creating a new product and its images
        with the validated data from the user and user_id
        context passed from ProductViewSet
        """
        uploaded_images=validated_data.pop('upload_image')
        print("This is the uploaded images ",uploaded_images)
        user_id=self.context['user_id']

        product=(
            Product.objects.create(
                user_id=user_id,
                **validated_data
                )
        )
        
        # ! For Creating the Product Images 
        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)

        return product

