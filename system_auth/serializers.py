from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.settings import api_settings

from account.models import Account
from currencies.models import Currency
from .models import SystemUser


class SystemUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    account_currency = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(),
        write_only=True,
        required=True
    )

    class Meta:
        model = SystemUser
        fields = ('id', 'password', 'email', 'username', 'first_name', 'last_name', 'account_currency')

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return make_password(value)

    def create(self, validated_data):
        account_currency = validated_data.pop('account_currency')
        with transaction.atomic():
            instance = super(SystemUserSerializer, self).create(validated_data)
            Account.objects.create(user=instance, currency=account_currency)
        return instance


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def authenticate(self):
        user = authenticate(**self.validated_data)
        if not user:
            raise serializers.ValidationError({
                api_settings.NON_FIELD_ERRORS_KEY: ['wrong email or password'],
            })
        return user
