
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('users/<str:username>', views.viewuser, name="viewuser"),
    path('newpost', views.newpost, name="newpost"),
    path('editpost', views.edit, name='edit'),
    path('following', views.following, name='following')
]
