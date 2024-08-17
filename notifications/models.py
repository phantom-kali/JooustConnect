# from django.db import models
from django.urls import reverse
<<<<<<< HEAD

=======
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
# from users.models import User

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

<<<<<<< HEAD

class Notification(models.Model):
    USER_CHOICES = (
        ("DM", "Direct Message"),
        ("GROUP", "Group Message"),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    content = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(
        max_length=5, choices=USER_CHOICES, default="DM"
    )
    related_id = models.IntegerField()  # This will store the DM or Group ID

    def get_redirect_url(self):
        if self.notification_type == "DM":
            return f"/messaging/{self.related_id}/"
        elif self.notification_type == "GROUP":
            return f"/groups/{self.related_id}/"
        return reverse("notifications")  # Default redirect
=======
class Notification(models.Model):
    USER_CHOICES = (
        ('DM', 'Direct Message'),
        ('GROUP', 'Group Message'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=5, choices=USER_CHOICES, default='DM')
    related_id = models.IntegerField()  # This will store the DM or Group ID

    def get_redirect_url(self):
        if self.notification_type == 'DM':
            return f'/messaging/{self.related_id}/'
        elif self.notification_type == 'GROUP':
            return f'/groups/{self.related_id}/'
        return reverse('notifications')  # Default redirect
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
