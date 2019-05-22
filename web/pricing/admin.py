from django.contrib import admin

from .models import *
# Register your models here.


class ShopAdmin(admin.ModelAdmin):
    list_display = ['title', 'currency', 'country', 'url']


class CountryAdmin(admin.ModelAdmin):
    list_display = ['title']


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Shop, ShopAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Country, CountryAdmin)
