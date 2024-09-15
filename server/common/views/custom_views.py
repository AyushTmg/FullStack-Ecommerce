
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet



class ReadCreateDeleteViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    pass