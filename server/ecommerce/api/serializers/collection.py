from ...models import Collection
from rest_framework import serializers


# !Collection Serializer
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title']
