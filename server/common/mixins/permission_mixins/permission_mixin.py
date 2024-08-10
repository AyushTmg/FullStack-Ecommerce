from rest_framework import permissions 
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from permissions import IsObjectUserOrAdminUserElseReadOnly


class IsAdminOrReadOnlyPermissionMixin:
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()]
    
class IsObjectUserOrAdminUserElseReadOnlyPermissionMixin:
    permission_classes=[IsObjectUserOrAdminUserElseReadOnly]

class AllowAnyPermissonMixin:
    permission_classes=[AllowAny]

class IsAuthenticatedPermissionMixin:
    permission_classes=[IsAuthenticated] 

class AdminPermissionMixin:
    permission_classes=[IsAdminUser]

