from django.utils import timezone
from django.db import transaction
from rest_framework import response
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import decorators
from rest_framework import filters
from currencies.models import CurrencyPairValue
from order.filters import OrderFilter

from .serializers import OrderSerializer
from .models import Order


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = (filters.DjangoFilterBackend, )
    filter_class = OrderFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def filter_queryset(self, queryset):
        queryset = queryset.filter(user=self.request.user)
        if self.action == 'close':
            queryset = queryset.filter(status=Order.ORDER_STATUS_OPENED)
        return super(OrderViewSet, self).filter_queryset(queryset)

    @decorators.detail_route(methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def close(self, request, *args, **kwargs):
        order = self.get_object()
        order.end_time = timezone.now()
        end_value = CurrencyPairValue.objects.filter(currency_pair=order.currency_pair).first()
        order.end_value = end_value
        order.status = Order.ORDER_STATUS_CLOSED
        amount = order.amount
        if order.type == Order.ORDER_TYPE_LONG:
            amount *= end_value.bid
        else:
            initial_amount = amount / order.start_value.bid
            debt_amount = initial_amount * end_value.ask
            amount -= debt_amount
        with transaction.atomic():
            order.user.account.change_amount_after_order(amount)
            order.save()
        serializer = self.serializer_class(order)
        return response.Response(
            data=serializer.data
        )
