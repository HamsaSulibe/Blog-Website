from django.conf import settings
from django.db import models


class Post(models.Model):
    """
    Represents a blog post created by a user.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # Default ordering: newest first

    def __str__(self):
        """
        String representation of the Post object.
        Example: "username:Post Title"
        """
        return f"{self.author.username}:{self.title}"

    def is_liked_by(self, user):
        """
        Check if the given user has liked this post.

        Args:
            user (User): The user to check.

        Returns:
            bool: True if the user liked this post, False otherwise.
        """
        return self.likes.filter(user=user).exists()


class Follow(models.Model):
    """
    Represents a following relationship between two users.
    follower -> following
    """

    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following"
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Prevent duplicate follows (follower cannot follow the same user twice)
            models.UniqueConstraint(fields=["follower", "following"], name="unique_follow"),

            # Prevent a user from following themselves
            models.CheckConstraint(
                check=~models.Q(follower=models.F("following")),
                name="no_self_follow"
            ),
        ]


class Like(models.Model):
    """
    Represents a 'like' reaction from a user on a post.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Prevent the same user from liking the same post more than once
            models.UniqueConstraint(fields=["user", "post"], name="unique_like")
        ]

    def __str__(self):
        """
        String representation of the Like object.
        Example: "username liked Post Title"
        """
        return f"{self.user.username} liked {self.post.title}"
