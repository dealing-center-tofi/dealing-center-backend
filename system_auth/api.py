from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import response
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import decorators

from dealing_center.utils import permissions as app_permissions

from .models import SystemUser, SecretQuestion
from .serializers import SystemUserSerializer, EmailLoginSerializer, RecoveryPasswordByEmailSerializer, \
    RecoveryPasswordSerializer, SecretQuestionSerializer


class SystemUserViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [app_permissions.IsUserAuthenticated, app_permissions.IsSelfUser]
    serializer_class = SystemUserSerializer
    queryset = SystemUser.objects.all()

    def get_object(self):
        lookup = self.lookup_url_kwarg or self.lookup_field
        if self.kwargs[lookup] == 'me':
            self.kwargs[lookup] = self.request.user.id
        return super(SystemUserViewSet, self).get_object()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = {'Token': Token.objects.get(user=serializer.instance)}
        return response.Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = EmailLoginSerializer

    @decorators.list_route(methods=['POST'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        user = self.authenticate_user()
        self.check_object_permissions(request, user)
        user_serializer = SystemUserSerializer(instance=user, context={'request': self.request})

        token = Token.objects.filter(user=user).first()
        if not token:
            token = Token.objects.create(user=user)
        headers = {'Token': token}

        return response.Response(
            data=user_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def authenticate_user(self):
        login_serializer = self.get_serializer(data=self.request.data)
        login_serializer.is_valid(raise_exception=True)
        return login_serializer.authenticate()

    @decorators.list_route(methods=['DELETE'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        request.auth.delete()
        return response.Response(None, status=status.HTTP_204_NO_CONTENT)

    @decorators.list_route(methods=['post'], permission_classes=[permissions.AllowAny])
    def password_recovery(self, request, **kwargs):
        serializer = RecoveryPasswordByEmailSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = SystemUser.objects.get(email__iexact=serializer.validated_data.get('email'))
            user.send_recovery_password_mail()
        except SystemUser.DoesNotExist:
            pass
        return response.Response()

    @decorators.list_route(methods=['post'], permission_classes=[permissions.AllowAny])
    def password_recovery_confirm(self, request, **kwargs):
        serializer = RecoveryPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = force_text(urlsafe_base64_decode(serializer.validated_data['uidb64']))
        user = SystemUser.objects.get(pk=uid)
        user.password = serializer.validated_data['password']
        user.save()

        return response.Response(status=status.HTTP_200_OK)


class SecretQuestionViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = SecretQuestionSerializer
    queryset = SecretQuestion.objects.all().order_by('?')
