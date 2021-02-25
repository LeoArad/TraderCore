from rest_framework import serializers
from .models import Post, PostsLikes
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework.response import Response


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'user_name', 'first_name', 'last_name', 'number_of_likes')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'date_created', 'user_created')
        extra_kwargs = {'user_created': {'read_only': True, 'required': False}}

    def create(self, validated_data):
        post = Post()
        print(validated_data)
        post.user_created = self.context['request']._user
        post.content = validated_data.get('content')
        post.title = validated_data.get('title')
        post.save()
        return post


class PostLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostsLikes
        fields = ('id', 'post', 'user', 'is_like')


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.username = validated_data.get('email')
        user.set_password(password)
        try:
            user.save()
        except IntegrityError:
            return {}
        return user