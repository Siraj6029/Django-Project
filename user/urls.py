from django.urls import path
from user.views import GetUserView, CreateUserView

urlpatterns = [
    path("user/", GetUserView.as_view(), name="user"),
    path("register/", CreateUserView.as_view(), name="CreateUser"),
]
