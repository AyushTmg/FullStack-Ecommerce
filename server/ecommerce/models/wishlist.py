from django.conf import settings
from django.db import models
from common.models import UUIDModel


class Wishlist(UUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('ecommerce.Product', on_delete=models.CASCADE, related_name='wishlist')
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} wishlist {self.product.title}"
