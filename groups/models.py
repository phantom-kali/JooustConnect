from django.db import models
from users.models import User

<<<<<<< HEAD

class Group(models.Model):
    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("private", "Private"),
        ("secret", "Secret"),
    ]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name="joined_groups")
    created_at = models.DateTimeField(auto_now_add=True)
    admins = models.ManyToManyField(User, related_name="admin_groups", blank=True)
    visibility = models.CharField(
        max_length=10, choices=VISIBILITY_CHOICES, default="public"
    )
    category = models.CharField(max_length=50, blank=True)
    tags = models.CharField(
        max_length=200, blank=True
    )  # Store tags as comma-separated values

    def __str__(self):
        return self.name


class GroupJoinRequest(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="join_requests"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("group", "user")


class GroupPost(models.Model):
    group = models.ForeignKey(Group, related_name="posts", on_delete=models.CASCADE)
=======
class Group(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('secret', 'Secret'),
    ]
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(User, related_name='joined_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    admins = models.ManyToManyField(User, related_name='admin_groups', blank=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    category = models.CharField(max_length=50, blank=True)
    tags = models.CharField(max_length=200, blank=True)  # Store tags as comma-separated values
    
    def __str__(self):
        return self.name

class GroupJoinRequest(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('group', 'user')

class GroupPost(models.Model):
    group = models.ForeignKey(Group, related_name='posts', on_delete=models.CASCADE)
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    n_views = models.PositiveIntegerField(default=0)
<<<<<<< HEAD
    likes = models.ManyToManyField(User, related_name="liked_group_posts", blank=True)


class GroupMessage(models.Model):
    group = models.ForeignKey(Group, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User, related_name="sent_group_messages", on_delete=models.CASCADE
    )
=======
    likes = models.ManyToManyField(User, related_name='liked_group_posts', blank=True)

class GroupMessage(models.Model):
    group = models.ForeignKey(Group, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_group_messages', on_delete=models.CASCADE)
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
