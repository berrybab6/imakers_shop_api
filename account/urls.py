from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path("", views.UserCreateView.as_view(), name="post users"),
    # path("detail/", views.UserDetailView.as_view(), name="User detail"),
    # path("user_role/<int:pk/", views.UserRoleView.as_view(), name="User by role"),
    path("login/", views.LoginUserView.as_view(), name="login user"),
    path("users/", views.GetAllUserView.as_view(), name="all users"),
    
    path("detail/", views.UserDetailView.as_view(), name="User detail"),
    # path("user_role/<int:pk/", views.UserRoleView.as_view(), name="User by role"),
    # path("login/", views.LoginUserView.as_view(), name="login user"),
    path('changePassword/', views.ChangePassword.as_view(), name="change Password"),
    # # path('upload/', views.ImageRelated.as_view(), name="ImageRelated"),
    path('images/<str:pk>/', views.ImageAPIView.as_view()),
    path('business_id/<str:pk>/', views.BusinessImageAPIView.as_view()),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
