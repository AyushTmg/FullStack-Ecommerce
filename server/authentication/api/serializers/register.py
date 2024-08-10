from ...models.user import ( User  ) 
from utils.exception import CustomException as ce

from django.db import transaction
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers






#! Serializer for User Registration 
class UserRegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )
    password_confirmation=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )


    class Meta:
        model=User 
        fields=[
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password_confirmation'
        ]


    def validate(self, attrs):
        """
        Ensures the password and password_confirmation 
        passed to a serializer is the same
        """
        password=attrs.get('password')
        password_confirmation=attrs.get('password_confirmation')

        if password!=password_confirmation:
            raise ce(
                message="Form Validation Error",
                errors={
                "password": [
                        "The two password field doesn't match."
                ],
                "password_confirmation": [
                        "The two password field doesn't match."
                ]
                }
            )
        
        return attrs
    
    
    def create(self,validated_data):
        """
        Over Riding the create method for user registration
        """
        try:
            with transaction.atomic():
                user=User.objects.create(
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    username=validated_data['username'],
                    email=validated_data['email'],
                )

                user.set_password(validated_data['password'])
                user.save()
                return user 
            
        except Exception as e:
            print(f"error --> {e}")
            raise ce(
                message="Somme Error occoured during registration"
                )
    
