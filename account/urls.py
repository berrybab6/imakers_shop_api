from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path("", views.UserCreateView.as_view(), name="post users"),
    # path("detail/", views.UserDetailView.as_view(), name="User detail"),
    # path("user_role/<int:pk/", views.UserRoleView.as_view(), name="User by role"),
    path("login/", views.LoginUserView.as_view(), name="login user"),
    path("users/", views.GetAllUserView.as_view(), name="all users")
    # path('changePassword/', views.ChangePassword.as_view(), name="change Password"),

]