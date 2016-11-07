from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import response
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import decorators

from dealing_center.utils import permissions as app_permissions

from .models import SystemUser
from .serializers import SystemUserSerializer, EmailLoginSerializer


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
