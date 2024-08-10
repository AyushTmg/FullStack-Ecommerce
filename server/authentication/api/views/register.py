from utils.response import CustomResponse as cr


from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_201_CREATED


from ..serializers import ( 
    UserRegistrationSerializer,
)



# ! View For User Registration 
class UserRegistrationView(APIView):
    serializer_class=UserRegistrationSerializer
    permission_classes=[AllowAny]

    def post(self,request) :
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return cr.success(
                message="Your account has been successfully registered",
                status=HTTP_201_CREATED
            )
        return cr.error(
            message="Form Validation Error",
            errors=serializer.errors
            )