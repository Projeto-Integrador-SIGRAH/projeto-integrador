from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    UserLoginAPI,
    UserLogoutAPIView,
    UserModelViewSet,
    UserRegistrationAPIView,
)

urlpatterns = [
    path("login/", UserLoginAPI.as_view(), name="login"),
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("logout", UserLogoutAPIView.as_view(), name="logout"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

router = routers.SimpleRouter()
router.register("", UserModelViewSet, basename="user")
urlpatterns += router.urls
