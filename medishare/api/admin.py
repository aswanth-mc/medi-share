from django.contrib import admin
from .models import ShoppingCart, CartItem, RecentlyViewed


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'get_total_items', 'get_total_quantity')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'

    def get_total_quantity(self, obj):
        return obj.get_total_quantity()
    get_total_quantity.short_description = 'Item Count'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'donation', 'quantity', 'added_at', 'get_availability')
    list_filter = ('added_at', 'updated_at', 'cart__user')
    search_fields = ('donation__medicine_name', 'cart__user__username')
    readonly_fields = ('added_at', 'updated_at')

    def get_availability(self, obj):
        return obj.get_availability()
    get_availability.short_description = 'Available'


@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ('user', 'donation', 'viewed_at')
    list_filter = ('viewed_at', 'user')
    search_fields = ('donation__medicine_name', 'user__username')
    readonly_fields = ('viewed_at',)
