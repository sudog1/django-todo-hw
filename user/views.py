from django.shortcuts import render, redirect
from config.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from .models import UserModel
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed


def signup_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return render(request, 'user/signup.html')
        else:
            if get_user_model().objects.filter(username=username).exists():
                return render(request, 'user/signup.html', {'error_message': '존재하는 아이디입니다.'})
            else:
                UserModel.objects.create_user(username=username, password=password, email=email)
                return redirect(reverse('user:signin'))
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

def signin_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        auth_user = auth.authenticate(username=username, password=password)
        if auth_user:
            auth.login(request, auth_user)
            return redirect(LOGIN_REDIRECT_URL)
        else:
            return redirect(reverse('user:signin'))
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@login_required
def logout_view(request):
    auth.logout(request)
    return redirect(LOGOUT_REDIRECT_URL)
