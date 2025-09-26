from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .models import Post, Like, Follow
from .serializers import UserSerializer, PostSerializer, LikeSerializer, FollowSerializer

# User API
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
   # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_permissions(self):
        if self.action == 'create':  # Sign Up
            return [permissions.AllowAny()]
        elif self.action == 'list':  # GET all users
            return [permissions.AllowAny()]
        elif self.action == 'retrieve':  # GET single user
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
# Post API
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

