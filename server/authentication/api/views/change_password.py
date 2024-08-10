
from utils.response import CustomResponse as cr

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..serializers import ( 
    UserChangePasswordSerializer,
)



# ! View For Changing Password
class UserChangePasswordView(APIView):
    serializer_class=UserChangePasswordSerializer
    permission_classes=[IsAuthenticated]

    def post(self,request):
        user=request.user
        serializer=self.serializer_class(data=request.data,context={'user':user})
        serializer.is_valid(raise_exception=True)

        return cr.success(
            message="Password changed successfully"
        )