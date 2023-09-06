from django.shortcuts import render, redirect
from django.urls import reverse
from config.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed


def signup_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse("todo:home"))
        else:
            return render(request, "user/signup.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        # profile change
        if request.user.is_authenticated:
            user = request.user
            if username != user.username:
                if get_user_model().objects.filter(username=username).exists():
                    return render(
                        request, "user/profile.html", {"error_message": "존재하는 아이디입니다."}
                    )
                user.username = username
            if email != user.email:
                user.email = email
            user.save()
            return redirect(reverse("user:profile"))

        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if get_user_model().objects.filter(username=username).exists():
            return render(
                request, "user/signup.html", {"error_message": "존재하는 아이디입니다."}
            )
        elif password != password2:
            return render(
                request, "user/signup.html", {"error_message": "비밀번호를 확인해주세요."}
            )
        else:
            user = get_user_model().objects.create_user(
                username=username,
                password=password,
                email=email,
            )
            auth.login(request, user)
            return redirect(LOGIN_REDIRECT_URL)
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


def signin_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse("todo:home"))
        else:
            return render(request, "user/signin.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        auth_user = auth.authenticate(username=username, password=password)
        if auth_user:
            auth.login(request, auth_user)
            return redirect(LOGIN_REDIRECT_URL)
        else:
            return render(
                request, "user/signin.html", {"error_message": "아이디와 비밀번호를 확인해주세요."}
            )
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def logout_view(request):
    auth.logout(request)
    return redirect(LOGOUT_REDIRECT_URL)


# profile_picture
@login_required
def profile_view(request):
    if request.method == "GET":
        return render(request, "user/profile.html")
    elif request.method == "POST":
        user = request.user
        profile_picture = request.FILES.get("profile_picture")
        user.profile_picture = profile_picture
        user.save()
        return redirect(reverse("user:profile"))
    else:
        return HttpResponseNotAllowed(["GET", "POST"])
