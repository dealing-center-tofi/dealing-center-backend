from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.settings import api_settings

from account.models import Account
from currencies.models import Currency
from .models import SystemUser, SecretQuestion


class SecretQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecretQuestion
        fields = ('id', 'question_text', )


class SystemUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    account_currency = serializers.PrimaryKeyRelatedField(
        queryset=Currency.objects.all(),
        write_only=True,
        required=True
    )
    birth_date = serializers.DateField()
    secret_question = SecretQuestionSerializer(read_only=True)
    secret_question_id = serializers.PrimaryKeyRelatedField(
        queryset=SecretQuestion.objects.all(),
        write_only=True,
        required=True,
        source='secret_question'
    )

    class Meta:
        model = SystemUser
        fields = ('id', 'password', 'email', 'first_name',
                  'second_name', 'last_name', 'birth_date',
                  'secret_question', 'secret_question_id',
                  'answer_secret_question', 'account_currency')

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


class RecoveryPasswordByEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ['email']
        model = SystemUser


class RecoveryPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        fields = ('password', 'token', 'uidb64', )

    def validate(self, validated_data):
        uid = force_text(urlsafe_base64_decode(validated_data.get('uidb64')))
        user = SystemUser.objects.filter(pk=uid).first()
        if not user:
            raise serializers.ValidationError('Bad uidb64')
        if not default_token_generator.check_token(user, validated_data.get('token')):
            raise serializers.ValidationError('Bad token')
        return validated_data

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return make_password(value)
