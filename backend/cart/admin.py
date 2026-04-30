from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'session_key')
    readonly_fields = ('created_at',)

# CartItem hidden from admin
# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'cart', 'product', 'quantity')
#     list_filter = ('cart__user',)
#     search_fields = ('product__name',)
