from ...models.user import ( User  ) 
from ...tasks import  password_reset_task
from utils.exception import CustomException as ce 


from django.utils.encoding import smart_str, force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode


from rest_framework import serializers



#! Serializer for Sending Password Reset Email
class SendResetPasswordEmailSerializer(serializers.Serializer):
      email=serializers.EmailField()

      def validate(self, attrs):
        """
        Check If The Provided Email Is Registered or 
        not and if yes it also sends  a reset link  that email 
        """
        email=attrs.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ce(
                message="User with the given email doesn't exist"
            )

        uid=urlsafe_base64_encode(force_bytes(user.id))
        token=PasswordResetTokenGenerator().make_token(user)
        link=f'http://127.0.0.1:8000/api/auth/reset-password/{uid}/{token}/'
        subject="Resetting Password"
        email=user.email

        data={
            "subject":subject,
            "link":link,
            "to_email":email
        }
        password_reset_task.delay(data)

        return attrs
       




#! Serializer for Resetting Password 
class PasswordResetSerializer(serializers.Serializer):
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


    def validate(self, attrs):
        """
        Validate UID and Token from url params
        and set new passsword for the user
        """
        password=attrs.get('password')
        password_confirmation=attrs.get('password_confirmation')

        uid=self.context['uid']
        token=self.context['token']
        id=smart_str(urlsafe_base64_decode(uid))

        if password != password_confirmation:
            raise ce(
                message="Two password field doesn't match"
            )
        
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise ce(
                message="User not found"
            )
        
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise ce(
                message="Token Expired or Invalid"
            )
        
        user.set_password(password)
        user.save()

        return attrs


