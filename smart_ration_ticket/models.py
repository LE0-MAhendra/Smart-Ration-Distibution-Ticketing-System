from django.db import models
from django.contrib.auth.models import User
from datetime import date, time


class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agent_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    center_code = models.CharField(max_length=20)
    address = models.TextField()
    availability_days = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("available", "Service Available"),
            ("offline", "Offline"),
            ("error", "Network Error"),
        ],
        default="available",
    )

    def __str__(self):
        return self.agent_name


class DistributionSession(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    start_time = models.TimeField(default=time(9, 0))  # default 9:00 AM
    end_time = models.TimeField(default=time(17, 0))  # default 5:00 PM
    status = models.CharField(
        max_length=20,
        choices=[("open", "Open"), ("closed", "Closed"), ("cancelled", "Cancelled")],
        default="open",
    )
    current_token = models.PositiveIntegerField(default=1)
    max_tokens = models.PositiveIntegerField(default=50)  # new field added

    def __str__(self):
        return f"{self.supplier.agent_name} - {self.date}"


class UserBooking(models.Model):
    ration_card_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, null=True, blank=True)
    date = models.DateField()
    token_number = models.PositiveIntegerField()
    session = models.ForeignKey(DistributionSession, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[("open", "Open"), ("closed", "Closed"), ("cancelled", "Cancelled")],
        default="open",
    )

    def __str__(self):
        return f"{self.ration_card_number} - Token {self.token_number}"
