import uuid
from django.db import models 
# from cuser.fields import CurrentUserField
from django.utils import timezone


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True 
        ordering=['-created_at','-updated_at']


# class UserTrackedModel(models.Model):
#     created_by=CurrentUserField(
#         add_only=True,
#         related_name="%{app_label}s_%{class}s_created",
#         null=True
#     )
#     updated_by=CurrentUserField(
#         add_only=True,
#         related_name="%{app_label}s_%{class}s_updated",
#         null=True
#     )

#     class Meta:
#         abstract=True 


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)



class BaseModel(TimeStampedModel,SoftDeleteModel,UUIDModel):
    class Meta:
        abstract=True 
        ordering=['-created_at','-updated_at']





