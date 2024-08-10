from utils.response import CustomResponse as cr

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_404_NOT_FOUND

from ..serializers import ( 
    UserAccountDeleteSerializer
)



# ! View For Deleting User Account 
class UserAccountDeleteView(APIView):
    serializer_class=UserAccountDeleteSerializer
    permission_classes=[IsAuthenticated]


    def post(self,request):
        user=request.user

        # ! Calling serailizer to take data a validate it 
        serializer=self.serializer_class(data=request.data,context={'user':user})
        serializer.is_valid(raise_exception=True)

        # ! Calling a method to delete a user account
        user.delete_user_account()

        return cr.success(
            message="Your account has been successfullly deleted",
            status=HTTP_404_NOT_FOUND
        )