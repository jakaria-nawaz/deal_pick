from django.contrib import admin

from .models import *
# Register your models here.


class ShopAdmin(admin.ModelAdmin):
    list_display = ['title', 'currency', 'country', 'url']


class CountryAdmin(admin.ModelAdmin):
    list_display = ['title']


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['title']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'shop']
    readonly_fields = ['image']


class PriceAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'created_at']
    readonly_fields = ['product']


admin.site.register(Price, PriceAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Country, CountryAdmin)
