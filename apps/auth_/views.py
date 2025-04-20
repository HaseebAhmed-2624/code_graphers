from django.contrib.auth import get_user_model
from rest_framework import decorators, viewsets, status, permissions
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response

from apps.utils.mixins import ViewSetMixin
from . import serializers

UserModel = get_user_model()


class AuthViewSet(
    mixins.CreateModelMixin,
    ViewSetMixin.PartialUpdateModelMixin,
    viewsets.GenericViewSet,
):
    """User Specific auth apis"""

    queryset = UserModel.objects
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'deposit':
            return serializers.DepositSerializer
        return self.serializer_class

    def get_object(self):
        return super().get_object()

    def get_permissions(self):
        if self.action in ['register']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


    @decorators.action(detail=False, methods=["get"])
    def profile(self, request, *args, **kwargs):
        serializer = self.serializer_class(instance=request.user, context=self.get_serializer_context())
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @decorators.action(detail=False, methods=["post"])
    def register(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
