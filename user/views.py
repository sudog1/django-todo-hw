from django.shortcuts import render, redirect
from .models import UserModel
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/todo')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)

        if password != password2:
            return render(request, 'user/signup.html')
        else:
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html')
            else:
                UserModel.objects.create_user(username=username, password=password, email=email)
                return redirect('/user/sign-in')

def sign_in_view(request):
    if request.method == 'GET':
        is_auth = request.user.is_authenticated
        if is_auth:
            return redirect('/todo')
        else:
            return render(request, 'user/signin.html')
    elif request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        target = auth.authenticate(username=username, password=password)
        if target:
            auth.login(request, target)
            return redirect('/todo')
        else:
            return redirect('/user/sign-in')

@login_required
def logout_view(request):
    auth.logout(request)
    return redirect('/user/sign-in')
