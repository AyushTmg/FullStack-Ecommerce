
class UserAssignMixin:
    """ 
    To use this you need to pass user in the serializer context
    ########## Recommended ########## 
    ==> Use UserContextMixin which is made to specifically work with this 
    """
    def create(self,validated_data):
        validated_data['user']=self.context['user']
        return super().create(validated_data)
        