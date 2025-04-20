from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.utils.helpers.filters import Filters as f

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    def validate_password(self, value):
        validate_password(password=value, user=self.instance)
        return make_password(value, )

    class Meta:
        model = UserModel
        fields = ['id','email','username','password','first_name','last_name','balance']
        extra_kwargs = {
            "password": {"write_only": True},
        }

class DepositSerializer(serializers.Serializer):
    balance = serializers.FloatField(min_value=0)

class PasswordValidator(serializers.Serializer):
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        validate_password(password=attrs["password"], user=self._context["user"])
        return attrs
