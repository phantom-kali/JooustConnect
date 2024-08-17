from django.conf import settings
from django.db import models

<<<<<<< HEAD

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_messages",
        on_delete=models.CASCADE,
    )
=======
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
<<<<<<< HEAD
        ordering = ["timestamp"]
=======
        ordering = ['timestamp']
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
