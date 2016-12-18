import json

from datetime import timedelta

from redis import Redis
from celery.task import periodic_task

from dealing_center_settings.models import Setting
from account.models import Account
from order.serializers import OrderSerializer
from .models import Order
from currencies.models import CurrencyPairValue


def calculate_task_time():
    return json.loads(Setting.objects.get(name='check_orders_period').value)


def get_orders_profit(orders):
    profit = []
    for order in orders:
        currency_pair_value = CurrencyPairValue.objects.filter(currency_pair=order.currency_pair).first()
        profit.append(order.get_profit(currency_pair_value))
    return sum(profit), profit.index(min(profit))


@periodic_task(run_every=timedelta(**calculate_task_time()))
def check_orders():
    redis_app = Redis()

    for account in Account.objects.all():
        orders = list(Order.objects.filter(user=account.user, status=Order.ORDER_STATUS_OPENED))
        while len(orders) != 0:
            profit, min_profit_index = get_orders_profit(orders)
            funds = account.amount + profit
            if account.amount * 0.2 > funds:
                order = orders.pop(min_profit_index)
                order.close()

                serializer = OrderSerializer(order)
                data = json.dumps(serializer.data)

                redis_app.publish('tornado-orders_closing_delivery#orders_closing-user-%s#' % order.user_id,
                                  '["order closed", %s]' % data)
            else:
                break
