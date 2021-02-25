from django.contrib import admin
from .models import Post, PostsLikes

# Register your models here.
admin.site.register(Post)
admin.site.register(PostsLikes)
