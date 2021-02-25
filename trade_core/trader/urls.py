from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("posts", views.PostView, basename="Posts")
router.register("postslikes", views.PostsLikesView, basename="PostsLikes")

urlpatterns = [
    path('', include(router.urls)),
    path('userlikes/<int:user_id>', views.UserLikesView.as_view(), name='userlikes'),
    path('accounts/create/', views.UserCreate.as_view(), name='create_user'),
    path('next/user/<int:max_likes>', views.get_next_user_to_like, name='next_user'),
    path('next/posts/<int:user_id>', views.get_possible_posts_ids, name='possible_posts_ids')
]
