from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'total')

# OrderItem hidden from admin
# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'order', 'product', 'quantity', 'price')
#     list_filter = ('order__status',)
#     search_fields = ('product__name', 'order__id')
