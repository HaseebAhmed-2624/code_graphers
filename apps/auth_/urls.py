from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("", views.AuthViewSet, basename="auth_")

urlpatterns = [

    path('login/', TokenObtainPairView.as_view(), name='auth_token_refresh'),
    path('token/refresh/', TokenRefreshView.as_view(), name='auth_token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='auth_token_blacklist'),

]

urlpatterns += router.urls
