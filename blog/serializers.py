from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Like, Follow

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
# Post Serializer
class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = ["id", "title", "body", "created_at", "author"]


# Like Serializer 
class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]


# Follow Serializer
class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source="follower.username")
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "created_at"]
