from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('auth', views.auth, name='auth'),
    path("register", views.register_request, name="register"),
    path("auth", views.auth, name="auth"),
    path("login", views.login_request, name="login"),
    path('profile', views.profile, name='profile'),
    path('rating', views.rating, name='rating'),
    path('test', views.test, name='test'),
    path("logout", views.logout_request, name="logout"),
    path("password_reset", views.password_reset_request, name="password_reset")
]