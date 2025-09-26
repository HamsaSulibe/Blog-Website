from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Post, Like, Follow


class PostListView(ListView):
    """
    Display a paginated list of all posts on the home page.
    Adds a context variable 'liked_posts' containing the IDs of posts
    that the current user has liked (if authenticated).
    """
    model = Post
    template_name = "blog/index.html"
    paginate_by = 50
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        liked_posts = []
        if user.is_authenticated:
            liked_posts = set(
                Like.objects.filter(user=user).values_list("post_id", flat=True)
            )
        context["liked_posts"] = liked_posts
        return context


class FollowingFeedView(LoginRequiredMixin, ListView):
    """
    Display a feed of posts from users that the current user follows.
    Also provides context for liked posts, list of other users,
    and IDs of users that the current user is following.
    """
    model = Post
    template_name = "blog/following_feed.html"
    paginate_by = 10
    context_object_name = "posts"

    def get_queryset(self):
        return (
            Post.objects
            .filter(author__followers__follower=self.request.user)
            .select_related("author")
            .prefetch_related("likes")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        liked_posts = set(
            Like.objects.filter(user=user).values_list("post_id", flat=True)
        )
        context["liked_posts"] = liked_posts

        User = get_user_model()
        context["users"] = User.objects.exclude(id=user.id)

        context["following_ids"] = set(
            Follow.objects.filter(follower=user).values_list("following_id", flat=True)
        )
        return context


@login_required
def user_list(request):
    """
    Display a list of all users except the current one,
    along with the IDs of users the current user is following.
    """
    User = get_user_model()
    users = User.objects.exclude(id=request.user.id)

    following_ids = set(
        Follow.objects.filter(follower=request.user)
                      .values_list("following_id", flat=True)
    )

    return render(request, "blog/following.html", {
        "users": users,
        "following_ids": following_ids,
    })


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new post. The author is set automatically
    to the currently logged-in user.
    """
    model = Post
    fields = ["title", "body"]
    template_name = "blog/create_post.html"
    success_url = reverse_lazy("blog:index")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

#OFF
class AuthorRequiredMixin(UserPassesTestMixin):
    """
    Mixin that ensures only the author of a post can edit or delete it.
    """

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Update an existing post (author only)."""
    model = Post
    fields = ["title", "body"]
    template_name = "blog/edit_post.html"
    success_url = reverse_lazy("blog:index")


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """Delete an existing post (author only)."""
    model = Post
    template_name = "blog/confirm_delete.html"
    success_url = reverse_lazy("blog:index")


@method_decorator(require_POST, name="dispatch")
class ToggleLikeView(LoginRequiredMixin, View):
    """
    Toggle like/unlike for a given post.
    If the like does not exist, create it; otherwise, delete it.
    """
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
        return redirect(request.META.get("HTTP_REFERER") or reverse("blog:index"))


@method_decorator(require_POST, name="dispatch")
class ToggleFollowView(LoginRequiredMixin, View):
    """
    Toggle follow/unfollow for a given user.
    Prevents users from following themselves.
    """
    def post(self, request, user_id):
        User = get_user_model()
        target = get_object_or_404(User, pk=user_id)
        if target == request.user:
            raise PermissionDenied
        f, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            f.delete()
        return redirect(request.META.get("HTTP_REFERER") or reverse("blog:following"))


def signup(request):
    """
    Handle user registration.
    If the form is valid, create the user, log them in, and redirect to following feed.
    Otherwise, re-render the signup form with errors.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            return redirect("blog:following")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
