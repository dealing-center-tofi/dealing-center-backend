from django.contrib import admin

from .models import Currency, CurrencyPair, CurrencyPairValue


class CurrencyAdmin(admin.ModelAdmin):
    pass


class CurrencyPairAdmin(admin.ModelAdmin):
    pass


class CurrencyPairValueAdmin(admin.ModelAdmin):
    list_display = ('currency_pair', 'bid', 'ask', 'creation_time_format')

    def creation_time_format(self, obj):
        return obj.creation_time.strftime('%Y-%b-%d %H:%M:%S')
    creation_time_format.short_description = 'Creation time'


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyPair, CurrencyPairAdmin)
admin.site.register(CurrencyPairValue, CurrencyPairValueAdmin)
