from django.db import models
from django.conf import settings
from users.models import User

<<<<<<< HEAD

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=150)
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    video = models.FileField(upload_to="post_videos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    n_views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
=======
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=150)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    n_views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c

    is_boosted = models.BooleanField(default=False)
    boost_expires_at = models.DateTimeField(null=True, blank=True)

    @property
    def n_likes(self):
        return self.likes.count()

    @property
    def n_comments(self):
        return self.comments.count()

<<<<<<< HEAD

class PostView(models.Model):
    post = models.ForeignKey(Post, related_name="views", on_delete=models.CASCADE)
=======
class PostView(models.Model):
    post = models.ForeignKey(Post, related_name='views', on_delete=models.CASCADE)
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
<<<<<<< HEAD
        unique_together = ("post", "user")


class Report(models.Model):
    REPORT_TYPES = (
        ("spam", "Spam"),
        ("inappropriate", "Inappropriate Content"),
        ("harassment", "Harassment"),
        ("other", "Other"),
    )

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reports_made"
    )
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="reports")
=======
        unique_together = ('post', 'user')

class Report(models.Model):
    REPORT_TYPES = (
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('harassment', 'Harassment'),
        ('other', 'Other'),
    )

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_made')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='reports')
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Report by {self.reporter.username} on post {self.post.id}"

<<<<<<< HEAD

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
=======
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
>>>>>>> 20d5f52ef1d7d03304aa3abc20f5e37cc8590b2c
