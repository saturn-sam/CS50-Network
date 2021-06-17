
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("posts/edit/<int:id>", views.edit, name="edit"),
    path("likedislikepost", views.like_post, name='like-post'),
    path("following", views.following, name='following'),
]
