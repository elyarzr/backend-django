from django.contrib import admin
from .models import *


class ItemInline(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ['user','product','variant','size','color','quantity','price']


class orderAdmin(admin.ModelAdmin):
    list_display = ['user','email','f_name','l_name','address','create','paid','get_price']
    inlines = [ItemInline]


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code','start','end','discount','active']


admin.site.register(Order,orderAdmin)
admin.site.register(ItemOrder)
admin.site.register(Coupon,CouponAdmin)
