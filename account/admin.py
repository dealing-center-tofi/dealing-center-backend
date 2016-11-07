from django.contrib import admin

from .models import Account, Transfer


class AccountAdmin(admin.ModelAdmin):
    class Meta:
        model = Account


class TransferAdmin(admin.ModelAdmin):
    class Meta:
        model = Transfer


admin.site.register(Account, AccountAdmin)
admin.site.register(Transfer, TransferAdmin)
