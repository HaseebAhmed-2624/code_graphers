from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from . import models
from apps.auth_ import serializers as auth_serializers
from apps.utils.helpers.filters import Filters as f

UserModel = get_user_model()

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stocks
        fields='__all__'

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Transactions
        fields = '__all__'
        read_only_fields = ('updated_at','created_at',
                            'price_per_stock',)
