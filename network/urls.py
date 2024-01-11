
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post/", views.create_post, name="create_post"),

    #API Routes
   path('likes/<int:postID>/', views.like_toggle, name='like_toggle'),
   path('edit/<int:postID>/', views.edit, name='edit'),
   path('textarea/<int:postID>/', views.refresh_textarea, name='refresh_textarea'),
]