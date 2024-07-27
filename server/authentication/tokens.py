from rest_framework_simplejwt.tokens import RefreshToken

class CustomToken(RefreshToken):
    @classmethod
    def for_user(cls,user):
        token = super().for_user(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        token['email'] = user.email

        return token
    
def get_tokens_for_user(user):
    """
    Method which generates the tokens 
    """
    refresh = CustomToken.for_user(user)

    return {
        'refresh':str(refresh),
        'access': str(refresh.access_token),
    }
