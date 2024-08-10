from utils.response import CustomResponse as cr


from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


from ..serializers import ( 
    SendResetPasswordEmailSerializer,
    PasswordResetSerializer,
)




# ! View For Sending Password Reset  Link
class SendResetPasswordEmailView(APIView):
    serializer_class=SendResetPasswordEmailSerializer
    permission_classes=[AllowAny]

    def post(self,request) :
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return cr.success(
            message="Reset Password Email has been sent to the email"
        )
    



# !View For Resetting Password
class PassswordResetView(APIView):
    serializer_class=PasswordResetSerializer

    def post(self,request,**kwargs):
        uid=self.kwargs['uid']
        token=self.kwargs['token']

        serializer=self.serializer_class(data=request.data,context={'uid':uid,'token':token})
        serializer.is_valid(raise_exception=True)

        return cr.success(
            message="Password successfully changed"
        )

