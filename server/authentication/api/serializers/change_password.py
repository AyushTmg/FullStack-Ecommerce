from utils.exception import CustomException as ce 
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers





#! Serializer for Changing Password
class UserChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )
    new_password=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )
    new_password_confirmation=serializers.CharField(
        style={'input_type':'password'},
        write_only=True,
        validators=[validate_password]
    )
    

    def validate_old_password(self,value):
        """
        Validate old password of User before
        Changing it 
        """
        user = self.context["user"]
        if not user.check_password(value):
            raise ce(
                message="Current password doesn't match"
                )
        return value
    

    def validate(self, attrs):
        """
        Validate the new password and new password 
        confirmation and  Set new password for the user
        """
        old_password=attrs.get('old_password')
        new_password=attrs.get('new_password')
        new_password_confirmation=attrs.get('new_password_confirmation')

        if new_password != new_password_confirmation:
            raise ce(
                message='Two Passwords does not match'
            )
        
        if old_password==new_password:
            raise ce(
                message='New passwords cannot be similar to current password '
            )
        
        user=self.context['user']
        user.set_password(new_password)
        user.save()

        return attrs


