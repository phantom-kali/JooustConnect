from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    course = models.CharField(max_length=100, blank=True)  # Make this optional
    year = models.IntegerField(null=True, blank=True)  # Make this optional
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True)
    bio = models.TextField(blank=True)

    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following"
    )

    is_verified = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    premium_expiry = models.DateTimeField(null=True, blank=True)

    privacy_dms = models.BooleanField(default=False)
    privacy_posts = models.BooleanField(default=False)

    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
        ("system", "System"),
    ]
    theme_preference = models.CharField(
        max_length=10, choices=THEME_CHOICES, default="system"
    )

    def premium_expiring_soon(self):
        if not self.is_premium or not self.premium_expiry:
            return False
        return self.premium_expiry - timezone.now() <= timedelta(days=7)


class MpesaTransaction(models.Model):
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    transaction_date = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.transaction_id} - {self.amount}"
