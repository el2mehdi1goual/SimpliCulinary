from decimal import Decimal

from django.conf import settings
from django.db import models

from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cart",
    )
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user_id:
            return f"Cart of {self.user}"
        return f"Cart session {self.session_key or '?'}"

    @property
    def total(self) -> Decimal:
        total = Decimal("0")
        for item in self.items.select_related("product"):
            total += item.product.price * item.quantity
        return total.quantize(Decimal("0.01"))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"

    class Meta:
        unique_together = ("cart", "product")
