from django.shortcuts import render, redirect
from django.urls import reverse
from .models import TodoModel
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
        todo = TodoModel.objects.get(id=id)
        return render(request, "todo/detail.html", {"todo": todo})
    else:
        return HttpResponseNotAllowed(["GET"])


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
        todo = TodoModel.objects.get(id=id)
        if todo.author == request.user:
            return render(request, "todo/form.html", {"todo": todo})
        else:
            return redirect(reverse("todo:detail", args=[id]))
    elif request.method == "POST":
        todo = TodoModel.objects.get(id=id)
        todo.title = request.POST.get("title")
        todo.content = request.POST.get("content", "")
        if request.POST.get("is_completed"):
            todo.is_completed = True
        else:
            todo.is_completed = False
        todo.save()
        return redirect(reverse("todo:home"))
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def delete_view(request, id):
    if request.method == "GET":
        todo = TodoModel.objects.get(id=id)
        if todo.author == request.user:
            todo.delete()
            return redirect(reverse("todo:home"))
        else:
            return redirect(reverse("todo:detail", args=[id]))
    else:
        return HttpResponseNotAllowed(["GET"])


@login_required
def mypage_view(request):
    if request.method == "GET":
        todos = TodoModel.objects.filter(author=request.user).order_by("-created_at")
        return render(request, "todo/home.html", {"todos": todos})
    else:
        return HttpResponseNotAllowed(["GET"])
