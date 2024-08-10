from utils.exception import CustomException as ce 
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


#  ! Serializer for deleting user account permanently
class UserAccountDeleteSerializer(serializers.Serializer):
    password=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )


    def validate_password(self,value):
        """
        Validate password of User before deleting
        the users account
        """
        user = self.context["user"]
        if not user.check_password(value):
            raise ce(
                message="Current password doesn't match"
                )
        return value