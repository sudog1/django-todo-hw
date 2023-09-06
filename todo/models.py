from django.db import models
from user.models import UserModel


class TodoModel(models.Model):
    # (Todo) N:1 (User)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="todo")
    title = models.CharField(max_length=64)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    # (Todo) N:N (User)
    likes = models.ManyToManyField(UserModel, related_name="likes_todo", blank=True)


class CommentModel(models.Model):
    # (Comment) N:1 (User)
    author = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="comment"
    )
    # (Comment) N:1 (todo)
    todo = models.ForeignKey(
        TodoModel, on_delete=models.CASCADE, related_name="comment"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # (Comment) N:N (User)
    likes = models.ManyToManyField(UserModel, related_name="likes_comment", blank=True)
