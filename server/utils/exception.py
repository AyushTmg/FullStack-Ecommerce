from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST

class CustomException(APIException):
    
    def __init__(self,message=None, status=None,errors={}):
        if message is not None:
            self.detail = { 
                'success':False ,
                "message":message,
                'errors':errors
            }
            
        if status is not None:
            self.status_code = status


    # !If nothing is provided in in the constructer this exception will be returned instead
    status_code = HTTP_400_BAD_REQUEST 
    default_detail = {
        'success':False,
        "message": ""
    }
