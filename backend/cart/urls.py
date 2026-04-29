from django.urls import path

from .views import AddToCartView, CartDetailView

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_cart'),
]