from ...models import Review,Reply
from rest_framework import serializers
from common.mixins import UserAssignMixin


# !Reply Serializer
class ReplySerializer(UserAssignMixin,serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Reply
        fields=[
            'id',
            'user',
            'description',
        ]


    def create(self, validated_data):
        """ 
        Used for Creating a new product with the 
        validated data from the user and user_id
        and  review_id context passed from
        ReplyViewSet
        """
        validated_data['review_id']=self.context['review_id']
        return super().create(validated_data)




class ReviewSerailizer(UserAssignMixin,serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        fields=[
            'id',
            'user',
            'description',
        ]


    def create(self, validated_data):
        """ 
        Used for Creating a new product with the 
        validated data from the user and product_id
        context passed from ReviewViewSet
        """
        validated_data['product_id']=self.context['product_id']
        return super().create(validated_data)


