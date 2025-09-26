# from django.urls import path
# from .views import (
#     PostListView, FollowingFeedView,
#     PostCreateView, PostUpdateView, PostDeleteView,
#     ToggleLikeView, ToggleFollowView,
#     signup
# )

# app_name = "blog"

# urlpatterns = [
#     # Home page (all posts)
#     path("", PostListView.as_view(), name="index"),

#     # Following page (users + feed)
#     path("following/", FollowingFeedView.as_view(), name="following"),

#     # Create / Edit / Delete posts
#     path("post/new/", PostCreateView.as_view(), name="post_create"),
#     path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
#     path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),

#     # Like / Follow
#     path("post/<int:pk>/like/", ToggleLikeView.as_view(), name="toggle_like"),
#     path("user/<int:user_id>/follow/", ToggleFollowView.as_view(), name="toggle_follow"),

#     # Signup
#     path("signup/", signup, name="signup"),
# ]


from django.urls import path, include
from rest_framework import routers
from .views_api import UserViewSet, PostViewSet, LikeViewSet, FollowViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'follows', FollowViewSet)

urlpatterns = [
    # API routes
    path('', include(router.urls)),
]
