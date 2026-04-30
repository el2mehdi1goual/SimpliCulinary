from django.urls import path

from .views import CreateOrderView, OrderConfirmationView

urlpatterns = [
    path("create/", CreateOrderView.as_view(), name="order_create"),
    path(
        "confirmation/<int:pk>/",
        OrderConfirmationView.as_view(),
        name="order_confirmation",
    ),
]
