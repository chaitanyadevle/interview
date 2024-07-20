from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

from ..managers.base import BaseModelManager


class User(AbstractBaseUser):

    class Meta:
        db_table = "user"

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = list()

    name = models.CharField(max_length=512)
    username = models.CharField(max_length=512, unique=True)
    email = models.EmailField(max_length=512, null=True, blank=True)
    legal_name = models.CharField(max_length=128, null=True, blank=True, db_index=True)
    first_name = models.CharField(max_length=128, null=True, blank=True, db_index=True)
    emp_id = models.CharField(max_length=512, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_refresh_required = models.BooleanField(default=False)
    unsuccessful_login_count = models.PositiveIntegerField(default=0)
    indexes = [models.Index(fields=["legal_name"])]
    is_feed_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class BaseModel(models.Model):

    class Meta:
        abstract = True

    objects = BaseModelManager()
    created_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_creator", on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(
        User, related_name="%(app_label)s_%(class)s_modifier", on_delete=models.CASCADE
    )
    modified_on = models.DateTimeField(auto_now=True)
    deleted_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_deleter",
        on_delete=models.CASCADE,
    )
    deleted_on = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id or not self.created_on:  # type: ignore
            self.created_on = timezone.now()
        return super(BaseModel, self).save(*args, **kwargs)
