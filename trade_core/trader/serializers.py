import json
import requests
from .models import Post, PostsLikes
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework import serializers


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
        print(validated_data)
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.username = validated_data.get('email')
        if not self.validate_internal_email(user.username):
            raise serializers.ValidationError("This is not a valid email")
        user.set_password(password)
        try:
            user.save()
        except IntegrityError:
            return serializers.ValidationError("User with this email already exists")
        return user

    @staticmethod
    def validate_internal_email(email):
        if isinstance(email, str):
            print(f"in validation with {email}")
            base_url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=6a24635ab2b8cf115d614ff4953c7ec329da4389"
            try:
                print("before res")
                res = requests.get(base_url)
                print("afer")
            except Exception:
                return False

            if res.status_code == 200:
                print("In status")
                print(json.loads(res.text)["data"].get("status") != "invalid")
                return json.loads(res.text)["data"].get("status") != "invalid"
            return False
        else:
            return True

