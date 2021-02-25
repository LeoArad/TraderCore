import json
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from .models import Post, PostsLikes
from .serializers import PostSerializer, PostLikesSerializer, UsersSerializer


class PostView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostsLikesView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = PostsLikes.objects.all()
    serializer_class = PostLikesSerializer


class UserLikesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        content = {"count": len(PostsLikes.objects.filter(user_id=user_id))}
        return Response(content)


class UserCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UsersSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_next_user_to_like(request, max_likes):
    res = Post.objects.all().values('user_created_id').annotate(total=Count('id')).order_by('-total')
    if len(res) > 0:
        for i in res:
            current_likes_count = PostsLikes.objects.filter(user_id=i['user_created_id']).count()
            if current_likes_count < max_likes:
                return Response({"next_user_id": i['user_created_id'], "current_likes_count": current_likes_count})
    return Response({"There is no next user"}, status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def get_possible_posts_ids(request, user_id):
    users_ids = {i['user_created'] for i in
                 Post.objects.all().values('id', 'user_created').annotate(total=Count('postslikes__id')).filter(total=0)}
    res_list = []
    if len(users_ids) > 0:
        for id in users_ids:
            res_list.extend([i.id for i in Post.objects.filter(user_created_id=id)])
        if res_list:
            return Response({"possible_posts_ids": res_list})
    return Response({f"There is possible posts ids for user {user_id}"}, status.HTTP_404_NOT_FOUND)




