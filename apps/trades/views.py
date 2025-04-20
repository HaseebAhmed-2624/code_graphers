from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, permissions, response as r_, status
from . import serializers
from . import models
from apps.utils.mixins import ViewSetMixin
from . import tasks as background_tasks
from apps.utils import decorators as global_decorators

UserModel = get_user_model()


class StockViewSet(
    ViewSetMixin.AutoAddOwnerToRequestDataOnCreationAndUpdate,
    # ViewSetMixin.CacheListAndRetrieveMethodsMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """User Specific auth apis"""
    filterset_fields = ('id','owner', 'name')
    ordering_fields = ('date_added','date_last_modified')
    queryset = models.Stocks.objects
    serializer_class = serializers.StockSerializer

    def get_permissions(self):
        if self.action not in ['create']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        if self.action in ['update','partial_update']:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.all()

class TransactionViewSet(
    ViewSetMixin.RequestBodyValidationAndAtomicTransactionMixin,
    ViewSetMixin.AutoAddOwnerToRequestDataOnCreationAndUpdate,
    ViewSetMixin.CacheListAndRetrieveMethodsMixin,
    ViewSetMixin.RequiredFieldsMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    filterset_fields = ('id','owner', 'type','quantity','price_per_stock','stock')
    ordering_fields = ('date_added','date_last_modified')

    queryset = models.Transactions.objects
    serializer_class = serializers.TransactionSerializer

    @global_decorators.ensure_request_data_is_mutable
    @global_decorators.ensure_owner_is_added_to_request_data
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        background_tasks.create_transaction.delay(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return r_.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


