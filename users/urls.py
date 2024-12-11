from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LogoutView
from users.views import UserCreateView, UserProfileUpdateView
from .views import CustomLoginView


app_name = UsersConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path('profile/', UserProfileUpdateView.as_view(), name='profile_form'),
]
