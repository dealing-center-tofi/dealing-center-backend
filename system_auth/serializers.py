from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.settings import api_settings

from .models import SystemUser


class SystemUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = SystemUser
        fields = ('id', 'password', 'email', 'username', 'first_name', 'last_name', )

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return make_password(value)


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
