from django.contrib.auth import authenticate
from utils.response import CustomResponse as cr
from ...tokens import get_tokens_for_user


from rest_framework.views import APIView
from rest_framework.status import HTTP_401_UNAUTHORIZED


from ..serializers import ( 
    UserLoginSerializer,
)


# ! View For User Login
class UserLoginView(APIView):
    serializer_class=UserLoginSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email=serializer.data.get('email')
        password = serializer.validated_data.get('password')
        user=authenticate(
            email=email,
            password=password
        )

        if user is not  None:
            token=get_tokens_for_user(user)
            return cr.success(
                data=token,
                message="Logged in successfully",
            )
        
        else:
            return cr.error(
                message="Invalid credential. Please try again",
                status=HTTP_401_UNAUTHORIZED
            )