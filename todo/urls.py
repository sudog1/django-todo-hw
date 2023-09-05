from django.urls import path
from . import views

app_name = "todo"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("detail/<int:id>", views.detail_view, name="detail"),
    path("create/", views.create_view, name="create"),
    path("update/<int:id>", views.update_view, name="update"),
    path("delete/<int:id>", views.delete_view, name="delete"),
    path("mypage/", views.mypage_view, name="mypage"),
]
