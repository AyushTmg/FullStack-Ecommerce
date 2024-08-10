from rest_framework import serializers
from ...models.user import ( User  ) 


#! Serializer for User Login
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type':'password'}
    )

    class Meta:
        model=User
        fields=['email','password']

