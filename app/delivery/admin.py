from typing import Dict, Optional, Tuple
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Product,Order,OrderItem
from parler.admin import TranslatableAdmin


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ('title','slug','price','max_time','image')

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('title',)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','email','pay_type','address','created')
    list_filter = ('address',)
    search_fields = ('created',)
    inlines = [OrderItemInline]
