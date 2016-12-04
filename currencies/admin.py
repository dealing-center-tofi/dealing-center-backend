from django.contrib import admin

from .models import Currency, CurrencyPair, CurrencyPairValue, CurrencyPairValueHistory


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'price_to_usd')


class CurrencyPairAdmin(admin.ModelAdmin):
    pass


class CurrencyPairValueAdmin(admin.ModelAdmin):
    list_display = ('currency_pair', 'bid', 'ask', 'creation_time_format')
    list_filter = ('currency_pair', )
    readonly_fields = ('creation_time', )

    def creation_time_format(self, obj):
        return obj.creation_time.strftime('%Y-%b-%d %H:%M:%S')
    creation_time_format.short_description = 'Creation time'


class CurrencyPairValueHistoryAdmin(admin.ModelAdmin):
    list_display = ('currency_pair', 'period', 'open', 'high', 'low', 'close', 'creation_time_format')
    list_filter = ('currency_pair', 'period')

    def creation_time_format(self, obj):
        return obj.creation_time.strftime('%Y-%b-%d %H:%M:%S')
    creation_time_format.short_description = 'Creation time'

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(CurrencyPair, CurrencyPairAdmin)
admin.site.register(CurrencyPairValue, CurrencyPairValueAdmin)
admin.site.register(CurrencyPairValueHistory, CurrencyPairValueHistoryAdmin)
