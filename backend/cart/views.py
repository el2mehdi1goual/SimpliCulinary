from urllib.parse import quote

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView

from products.models import Product

from .models import Cart, CartItem


def _cart_matches_request(request, cart):
    if request.user.is_authenticated:
        return cart.user_id == request.user.id
    key = request.session.session_key
    return bool(key and cart.session_key == key)


class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        try:
            quantity = int(request.POST.get("quantity"))
            if quantity < 1:
                quantity = 1
        except (TypeError, ValueError):
            quantity = 1

        def redirect_detail(message):
            url = f"{reverse('product_detail', kwargs={'pk': product.pk})}?error={quote(message)}"
            return redirect(url)

        if product.stock < 1:
            return redirect_detail("Ce produit est en rupture de stock.")

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            cart, _ = Cart.objects.get_or_create(
                session_key=request.session.session_key
            )

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if created:
            new_qty = quantity
        else:
            new_qty = cart_item.quantity + quantity

        if new_qty > product.stock:
            return redirect_detail(
                "Quantité supérieure au stock disponible pour ce produit."
            )

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity = new_qty

        cart_item.save()
        return redirect("cart_detail")


class CartDetailView(DetailView):
    model = Cart
    template_name = "cart/detail_cart.html"
    context_object_name = "cart"

    def get_object(self):
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.create()

            session_key = self.request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

        return Cart.objects.prefetch_related("items__product").get(pk=cart.pk)


class CartItemUpdateView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id)
        if not _cart_matches_request(request, cart_item.cart):
            raise Http404()
        try:
            quantity = int(request.POST.get("quantity"))
        except (TypeError, ValueError):
            messages.error(request, "Quantité invalide.")
            return redirect("cart_detail")
        if quantity < 1:
            quantity = 1
        if quantity > cart_item.product.stock:
            messages.error(request, "la quantité est excédentaire")
            return redirect("cart_detail")

        cart_item.quantity = quantity
        cart_item.save()

        return redirect("cart_detail")


class CartItemDeleteView(DeleteView):
    model = CartItem
    template_name = "cart/cartitem_delete.html"
    success_url = reverse_lazy("cart_detail")
    context_object_name = "cartitem"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=self.request.user)
        else:
            session_key = self.request.session.session_key

            if not session_key:
                return CartItem.objects.none()

            cart = get_object_or_404(Cart, session_key=session_key)

        return CartItem.objects.filter(cart=cart)
