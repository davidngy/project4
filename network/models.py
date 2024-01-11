from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    creator = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="creator")
    post_content = models.TextField(max_length=500, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    likes_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.creator.username} - {self.date} {self.time}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_like")

    def __str__(self):
        return f"{self.user} - {self.post}"