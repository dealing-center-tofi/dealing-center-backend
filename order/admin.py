from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('start_time',)


admin.site.register(Order, OrderAdmin)
