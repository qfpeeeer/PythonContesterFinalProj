from django.urls import include, path
from . import views
from rest_framework import routers

from .views import NotificationView

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', views.index, name="index"),
    path('auth', views.auth, name='auth'),
    path("register", views.register_request, name="register"),
    path("auth", views.auth, name="auth"),
    path("login", views.login_request, name="login"),
    path('profile', views.profile, name='profile'),
    path('rating', views.rating, name='rating'),
    path("logout", views.logout_request, name="logout"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path("sort", views.sort, name="sort"),
    path('contest/<int:id>', views.contest, name="contest"),

    path('task/<int:id>', views.getTaskById, name='getTaskById'),
    path('contest/<int:contest_id>/task/<int:task_id>', views.getTaskByIdForContest, name='getTaskByIdForContest'),
    path('edit-task/<int:id>', views.editTask, name='edit-task'),
    path('suggest-new-task', views.suggest_task, name='suggest_task'),
    path('new-task', views.createTask, name='new_task'),
    path('new-test-cases', views.test_cases, name='new_test-cases'),
    path('task/run_sh/<int:type>', views.runscript, name='run_sh'),

    path('notify', views.notify, name="notify"),
    path('clearNotification', views.deleteNotification, name="clearNotification"),
    path('updateprofile',views.update, name="updateprofile"),

    path('notifications/', NotificationView.as_view()),

    path('', include(router.urls)),
]