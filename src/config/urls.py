from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView  # NOQA
from rest_framework_simplejwt.views import token_obtain_pair

from issues.api import get_issues, post_issues
from users.api import create_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("issues/", get_issues),
    path("issues/create", post_issues),
    path("users/", create_user),
    # Authentication
    path("auth/token/", token_obtain_pair),
    # path("auth/token/", TokenObtainPairView.as_view())
]
