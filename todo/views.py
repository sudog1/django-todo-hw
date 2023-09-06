from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.db.models import Count
from .models import CommentModel, TodoModel
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed


def home_view(request):
    if request.method == "GET":
        todos = TodoModel.objects.all().order_by("-created_at")
        return render(request, "todo/home.html", {"todos": todos})
    else:
        return HttpResponseNotAllowed(["GET"])


def detail_view(request, id):
    if request.method == "GET":
        todo = get_object_or_404(TodoModel, id=id)
        comments = todo.comment.annotate(count_likes=Count("likes")).order_by(
            "-count_likes", "-created_at"
        )
        return render(request, "todo/detail.html", {"todo": todo, "comments": comments})
    else:
        return HttpResponseNotAllowed(["GET"])


# todo
@login_required
def create_view(request):
    if request.method == "GET":
        return render(request, "todo/form.html")
    elif request.method == "POST":
        todo = TodoModel()
        todo.author = request.user
        todo.title = request.POST.get("title")
        todo.content = request.POST.get("content", "")
        todo.save()
        return redirect(reverse("todo:home"))
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def update_view(request, id):
    if request.method == "GET":
        todo = get_object_or_404(TodoModel, id=id)
        if todo.author == request.user:
            return render(request, "todo/form.html", {"todo": todo})
        else:
            return redirect(reverse("todo:detail", args=[id]))
    elif request.method == "POST":
        todo = get_object_or_404(TodoModel, id=id)
        todo.title = request.POST.get("title")
        todo.content = request.POST.get("content", "")
        if request.POST.get("completed"):
            todo.completed = True
        else:
            todo.completed = False
        todo.save()
        return redirect(reverse("todo:detail", args=[id]))
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def delete_view(request, id):
    if request.method == "POST":
        todo = get_object_or_404(TodoModel, id=id)
        if todo.author == request.user:
            todo.delete()
            return redirect(reverse("todo:home"))
        else:
            return redirect(reverse("todo:detail", args=[id]))
    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def mypage_view(request):
    if request.method == "GET":
        todos = request.user.todo.all().order_by("-created_at")
        return render(request, "todo/home.html", {"todos": todos})
    else:
        return HttpResponseNotAllowed(["GET"])


@login_required
def likes_view(request, id):
    if request.method == "POST":
        todo = get_object_or_404(TodoModel, id=id)
        user = request.user
        if user == todo.author:
            return redirect(reverse("todo:detail", args=[id]))
        if user in todo.likes.all():
            todo.likes.remove(user)
        else:
            todo.likes.add(user)
        return redirect(reverse("todo:detail", args=[id]))
    else:
        return HttpResponseNotAllowed(["POST"])


# comment
@login_required
def create_comment_view(request, todo_id):
    if request.method == "POST":
        todo = get_object_or_404(TodoModel, id=todo_id)
        content = request.POST.get("content", "")
        todo.comment.create(content=content, author=request.user)
        return redirect(reverse("todo:detail", args=[todo_id]))
    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def update_comment_view(request, todo_id, comment_id):
    if request.method == "GET":
        todo = get_object_or_404(TodoModel, id=todo_id)
        comment = get_object_or_404(CommentModel, id=comment_id)
        if comment.author == request.user:
            return render(
                request,
                "todo/comment_form.html",
                {"todo_id": todo_id, "comment": comment},
            )
        else:
            return redirect(reverse("todo:detail", args=[todo_id]))
    elif request.method == "POST":
        todo = get_object_or_404(TodoModel, id=todo_id)
        comment = get_object_or_404(CommentModel, id=comment_id)
        comment.content = request.POST.get("content", "")
        comment.save()
        return redirect(reverse("todo:detail", args=[todo_id]) + f"#댓글_{comment_id}")
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def delete_comment_view(request, todo_id, comment_id):
    if request.method == "POST":
        todo = get_object_or_404(TodoModel, id=todo_id)
        comment = get_object_or_404(CommentModel, id=comment_id)
        if comment.author == request.user:
            comment.delete()
        return redirect(reverse("todo:detail", args=[todo_id]))
    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def likes_comment_view(request, todo_id, comment_id):
    if request.method == "POST":
        todo = get_object_or_404(TodoModel, id=todo_id)
        comment = get_object_or_404(CommentModel, id=comment_id)
        user = request.user
        if user == comment.author:
            return redirect(reverse("todo:detail", args=[todo_id]))
        if user in comment.likes.all():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
        return redirect(reverse("todo:detail", args=[todo_id]) + f"#댓글_{comment_id}")
    else:
        return HttpResponseNotAllowed(["POST"])
