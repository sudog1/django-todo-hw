from django.urls import path
from . import views

app_name = "todo"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("detail/<int:id>", views.detail_view, name="detail"),
    # todo
    path("create/", views.create_view, name="create"),
    path("update/<int:id>", views.update_view, name="update"),
    path("delete/<int:id>", views.delete_view, name="delete"),
    path("mypage/", views.mypage_view, name="mypage"),
    path("likes/<int:id>", views.likes_view, name="likes"),
    # comment
    path("<int:todo_id>/create", views.create_comment_view, name="create_comment"),
    path("<int:todo_id>/update/<int:comment_id>", views.update_comment_view, name="update_comment"),
    path("<int:todo_id>/delete/<int:comment_id>", views.delete_comment_view, name="delete_comment"),
    path("<int:todo_id>/likes/<int:comment_id>", views.likes_comment_view, name="likes_comment"),
]
