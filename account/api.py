from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions

from dealing_center.utils import permissions as app_permissions

from .models import Account, Transfer
from .serializers import AccountSerializer, TransferSerializer


class AccountViewSet(mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, app_permissions.IsOwner]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    lookup_field = 'user__id'

    def get_object(self):
        lookup = self.lookup_url_kwarg or self.lookup_field
        if self.kwargs[lookup] == 'me':
            self.kwargs[lookup] = self.request.user.id
        return super(AccountViewSet, self).get_object()


class TransferViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransferSerializer
    queryset = Transfer.objects.all()

    def perform_create(self, serializer):
        account = self.request.user.account
        with transaction.atomic():
            transfer = serializer.save(account=account)
            account.change_amount_after_transfer(transfer)

    def filter_queryset(self, queryset):
        return queryset.filter(account__user=self.request.user)
