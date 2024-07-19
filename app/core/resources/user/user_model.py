from django.contrib.auth.models import AbstractBaseUser
from django.db import models


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
