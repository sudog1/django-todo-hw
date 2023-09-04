from django.shortcuts import render, redirect
from .models import TodoModel
from django.contrib.auth.decorators import login_required


def home_view(request):
    is_auth = request.user.is_authenticated
    if is_auth:
        return redirect('/todo')
    else:
        return redirect('/user/sign-in')


def todo_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            todo_list = TodoModel.objects.all().order_by('-created_at')
            return render(request, 'todo/home.html', {'todo_list': todo_list})
        else:
            return redirect('/user/sign-in')


def read_view(request, id):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            todo = TodoModel.objects.get(id=id)
            return render(request, 'todo/read.html', {'todo': todo})
        else:
            return redirect('/user/sign-in')

def create_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return render(request, 'todo/form.html')
        else:
            return redirect('/user/sign-in')
    elif request.method == 'POST':
        todo = TodoModel()
        todo.author = request.user
        todo.title = request.POST.get('title')
        todo.content = request.POST.get('content', '')
        todo.save()
        return redirect('/todo')
    

def update_view(request, id):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            todo = TodoModel.objects.get(id=id)
            if todo.author == request.user:
                return render(request, 'todo/form.html', {'todo': todo})
            else:
                return redirect(f'/todo/read/{id}')
        else:
            return redirect('/user/sign-in')
    elif request.method == 'POST':
        todo = TodoModel.objects.get(id=id)
        todo.title = request.POST.get('title')
        todo.content = request.POST.get('content', '')
        if 'is_completed' in request.POST:
            todo.is_completed = True
        else:
            todo_is_completed = False
        todo.save()
        return redirect('/todo')
    

@login_required
def delete_view(request, id):
    todo = TodoModel.objects.get(id=id)
    if todo.author == request.user:
        todo.delete()
        return redirect('/todo')
    else:
        return redirect(f'/todo/read/{id}')
    

def mypage_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            todo_list = TodoModel.objects.filter(author=request.user).order_by('-created_at')
            return render(request, 'todo/home.html', {'todo_list': todo_list})
        else:
            return redirect('/user/sign-in')