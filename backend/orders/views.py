from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.http import Http404
from django.shortcuts import redirect
from django.views import View

from cart.models import Cart

from .models import Order, OrderItem
from products.models import Product


class OrderCreateView(View):
    """Crée une commande à partir du panier (utilisateur connecté uniquement)."""

    def get(self, request):
        if not request.user.is_authenticated:
            messages.info(request, "Connectez-vous pour passer au paiement.")
            return redirect("cart_detail")

        cart = Cart.objects.filter(user=request.user).first()
        if cart is None or not cart.items.exists():
            messages.warning(request, "Votre panier est vide.")
            return redirect("cart_detail")

        items = list(cart.items.select_related("product"))
        for it in items:
            if it.quantity > it.product.stock:
                messages.error(
                    request,
                    f"Stock insuffisant pour « {it.product.name} ». Ajustez le panier.",
                )
                return redirect("cart_detail")

        with transaction.atomic():
            total = sum(it.product.price * it.quantity for it in items)
            order = Order.objects.create(
                user=request.user,
                total=total,
                shipping_address="A confirmer",
            )
            for it in items:
                OrderItem.objects.create(
                    order=order,
                    product=it.product,
                    quantity=it.quantity,
                    price=it.product.price,
                )
                Product.objects.filter(pk=it.product_id).update(
                    stock=F("stock") - it.quantity
                )
            cart.items.all().delete()

        messages.success(
            request,
            f"Commande n°{order.pk} enregistree (statut : {order.status}).",
        )
        return redirect("cart_detail")
