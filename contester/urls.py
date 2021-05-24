from django.urls import path
from . import views
from django.conf.urls import include, url

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
    path("password_reset", views.password_reset_request, name="password_reset"),

    path('task/<int:id>', views.getTaskById, name='getTaskById'),
    path('edit-task/<int:id>', views.editTask, name='edit-task'),

    path('suggest-new-task', views.suggest_task, name='suggest_task'),
    path('new-task', views.createTask, name='new_task'),
    path('new-test-cases', views.test_cases, name='new_test-cases'),
    path('list/', views.list, name='list'),
    path('task/run_sh', views.runscript, name='run_sh'),
]