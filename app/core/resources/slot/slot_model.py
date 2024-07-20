from core.models import BaseModel, User
from django.db import models


class SlotChoices(models.TextChoices):
    OPEN = "OPEN", "Open"
    BOOKED = "BOOKED", "Booked"
    PARTIAL_BOOKED = "PARTIAL", "Partial Booked"
    CANCELLED = "CANCELLED", "Cancelled"


class SubSlotChoices(models.TextChoices):
    BOOKED = "BOOKED", "Booked"
    CANCELLED = "CANCELLED", "Cancelled"


class Slot(BaseModel):

    class Meta:
        db_table = "slot"
        constraints = [
            models.CheckConstraint(
                name="%(class)s_status_valid",
                check=models.Q(slot_status__in=SlotChoices.values),
            ),
            models.UniqueConstraint(
                fields=["slot_recruiter", "slot_start_date_time", "slot_end_date_time"],
                condition=models.Q(slot_status="OPEN"),
                name="unique_open_slots_per_user",
            ),
        ]

    slot_timezone = models.CharField(
        max_length=50, null=True, blank=True
    )  # Store as TZ database name (e.g., 'Asia/Calcutta')
    slot_start_date_time = models.DateTimeField()
    slot_end_date_time = models.DateTimeField()
    slot_status = models.CharField(max_length=10, choices=SlotChoices.choices)
    slot_recruiter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="slots_as_recruiter"
    )

    def __str__(self):
        return f"Slot {self.slot_id}: {self.slot_start_date_time} to {self.slot_end_date_time}"  # type:  ignore


class SubSlot(BaseModel):

    class Meta:
        db_table = "subslot"
        constraints = [
            models.CheckConstraint(
                name="%(class)s_status_valid",
                check=models.Q(sub_slot_status__in=SubSlotChoices.values),
            ),
            models.UniqueConstraint(
                fields=["slot", "sub_slot_start_date_time", "sub_slot_end_date_time"],
                condition=models.Q(sub_slot_status="BOOKED"),
                name="unique_booked_sub_slots_per_user",
            ),
        ]

    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name="sub_slots")
    sub_slot_start_date_time = models.DateTimeField()
    sub_slot_end_date_time = models.DateTimeField()
    sub_slot_status = models.CharField(max_length=10, choices=SubSlotChoices.choices)
    sub_slot_booked_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="slots_as_hr",
    )
    sub_slot_booked_for = models.CharField(max_length=255)  # Candidate name or label

    def __str__(self):
        return f"Subslot {self.slot_id}: {self.slot_start_date_time} to {self.slot_end_date_time}"  # type:  ignore
