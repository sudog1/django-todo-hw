from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up_view),
    path('sign-in/', views.sign_in_view),
    path('logout/', views.logout_view),
]