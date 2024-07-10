from django.contrib.auth import authenticate
from utils.response.response import CustomResponse as cr


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.status import HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_404_NOT_FOUND


from .serializers import ( 
    UserRegistrationSerializer,
    UserActivationSerializer,
    UserLoginSerializer,
    UserChangePasswordSerializer,
    SendResetPasswordEmailSerializer,
    PasswordResetSerializer,
    UserAccountDeleteSerializer
)




#! Generates token manually
def get_tokens_for_user(user):
    """
    Method which generates the tokens 
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh':str(refresh),
        'access': str(refresh.access_token),
    }




# ! View For User Registration 
class UserRegistrationView(APIView):
    serializer_class=UserRegistrationSerializer
    permission_classes=[AllowAny]

    def post(self,request) -> Response:
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return cr.success(
            message="Registered successfully,Activation link has been sent to your email",
            status=HTTP_201_CREATED
        )





# ! View For User Activation
class UserActivationView(APIView):
    serializer_class=UserActivationSerializer

    def post(self,request,**kwargs)-> Response:
        uid=self.kwargs['uid']
        token=self.kwargs['token']
        serializer=self.serializer_class(data=request.data,context={'uid':uid,"token":token})
        serializer.is_valid(raise_exception=True)
        
        return cr.success(
            message="Your account has been successfully activated"
        )




# ! View For User Login
class UserLoginView(APIView):
    serializer_class=UserLoginSerializer

    def post(self,request)-> Response:
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email=serializer.data.get('email')
        password = serializer.validated_data.get('password')
        user=authenticate(email=email,password=password)

        if user is not  None:
            token=get_tokens_for_user(user)
            return cr.success(
                data=token,
                message="Logged in successfully",
            )
        
        else:
            return cr.error(
                message="Invalid Credential provided or Account is not active",
                status=HTTP_401_UNAUTHORIZED
            )
            




# ! View For Changing Password
class UserChangePasswordView(APIView):
    serializer_class=UserChangePasswordSerializer
    permission_classes=[IsAuthenticated]

    def post(self,request) -> Response:
        user=request.user
        serializer=self.serializer_class(data=request.data,context={'user':user})
        serializer.is_valid(raise_exception=True)

        return cr.success(
            message="Password changed successfully"
        )




# ! View For Sending Password Reset  Link
class SendResetPasswordEmailView(APIView):
    serializer_class=SendResetPasswordEmailSerializer
    permission_classes=[AllowAny]

    def post(self,request) -> Response:
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return cr.success(
            message="Reset Password Email has been sent to the email"
        )
    



# !View For Resetting Password
class PassswordResetView(APIView):
    serializer_class=PasswordResetSerializer

    def post(self,request,**kwargs) -> Response:
        uid=self.kwargs['uid']
        token=self.kwargs['token']

        serializer=self.serializer_class(data=request.data,context={'uid':uid,'token':token})
        serializer.is_valid(raise_exception=True)

        return cr.success(
            message="Password successfully changed"
        )




# ! View For Deleting User Account 
class UserAccountDeleteView(APIView):
    serializer_class=UserAccountDeleteSerializer
    permission_classes=[IsAuthenticated]


    def post(self,request)-> Response:
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