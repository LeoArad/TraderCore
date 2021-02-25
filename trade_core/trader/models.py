from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# class User(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     number_of_likes = models.IntegerField(default=0, auto_created=True)
#
#     def __str__(self):
#         return self.user_name if not any([self.first_name, self.last_name]) else f"{self.first_name} {self.last_name}"
#
#     def add_like(self):
#         self.number_of_likes += 1
#         self.save()
#
#     def remove_like(self):
#         if self.number_of_likes >= 0:
#             self.number_of_likes -= 1
#             self.save()


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    user_created = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    date_created = models.DateTimeField(auto_now=True)


class PostsLikes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)

    class Meta:
        unique_together = ('post', 'user',)

