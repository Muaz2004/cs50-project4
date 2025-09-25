
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    #path("allpost", views.view_posts, name="allpost"),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    path('unfollow', views.unfollow, name='unfollow'),
    path('following', views.following, name='following'),
    path("edit/<int:post_id>/", views.edit, name="edit"),
    path('like/<int:postId>/', views.like, name='like'),  
    path('get-liked-state/<int:postId>/', views.get_liked_state, name='get_liked_state'),

]
