from django.urls import path

from .views import (
    AddToCartView,
    CartDetailView,
    CartItemDeleteView,
    CartItemUpdateView,
)

urlpatterns = [
    path("add/<int:product_id>", AddToCartView.as_view(), name="add_cart"),
    path("", CartDetailView.as_view(), name="cart_detail"),
    path("<int:pk>/delete/", CartItemDeleteView.as_view(), name="cartItem_delete"),
    path("<int:pk>/update/", CartItemUpdateView.as_view(), name="cartItem_update"),
]
