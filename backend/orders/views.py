from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView

from cart.utils import get_cart

from .forms import OrderForm
from .models import Order, OrderItem
from products.models import Product


@method_decorator(login_required, name="dispatch")
class CreateOrderView(View):
    """Affiche le formulaire de commande (GET) et enregistre la commande (POST)."""

    template_name = "orders/shipping.html"

    def get(self, request):
        cart = get_cart(request)
        if not cart.items.exists():
            messages.warning(request, "Votre panier est vide.")
            return redirect("cart_detail")

        form = OrderForm()
        return render(
            request,
            self.template_name,
            {"form": form, "cart": cart},
        )

    def post(self, request):
        cart = get_cart(request)
        if not cart.items.exists():
            messages.warning(request, "Votre panier est vide.")
            return redirect("cart_detail")

        form = OrderForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {"form": form, "cart": cart},
            )

        items = list(cart.items.select_related("product"))
        for it in items:
            if it.quantity > it.product.stock:
                messages.error(
                    request,
                    f"Stock insuffisant pour « {it.product.name} ». Ajustez le panier.",
                )
                return render(
                    request,
                    self.template_name,
                    {"form": form, "cart": cart},
                )

        with transaction.atomic():
            total = sum(it.product.price * it.quantity for it in items)
            order = Order.objects.create(
                user=request.user,
                total=total,
                shipping_address=form.cleaned_data["shipping_address"],
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

        messages.success(request, f"Commande n°{order.pk} enregistrée.")
        return redirect("order_confirmation", pk=order.pk)


@method_decorator(login_required, name="dispatch")
class OrderConfirmationView(DetailView):
    model = Order
    template_name = "orders/confirmation.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            "items__product"
        )
