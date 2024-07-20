from core.models import BaseModel
from django.db import models


class UserTypeChoices(models.TextChoices):
    INTERVIEWER = "INTERVIEWER", "Interviewer"
    ADMIN = "ADMIN", "Admin"
    HR = "HR", "HR"


class UserType(BaseModel):
    class Meta:
        db_table = "usertype"
        constraints = [
            models.CheckConstraint(
                name="%(class)s_type_name_valid",
                check=models.Q(type_name__in=UserTypeChoices.values),
            )
        ]

    type_name = models.CharField(
        max_length=16, choices=UserTypeChoices.choices, unique=True
    )
    description = models.CharField(max_length=255, null=True, blank=True)
