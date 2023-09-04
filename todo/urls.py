from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view),
    path('todo/', views.todo_view),
    path('todo/read/<int:id>', views.read_view),
    path('todo/create/', views.create_view),
    path('todo/update/<int:id>', views.update_view),
    path('todo/delete/<int:id>', views.delete_view),
]