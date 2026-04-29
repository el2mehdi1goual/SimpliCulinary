from urllib.parse import quote

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from products.models import Product

from .models import Cart, CartItem


class AddToCartView(View):
    """POST : ajoute une ligne au panier (utilisateur connecté uniquement)."""

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)

        def redirect_detail(message):
            url = f"{reverse('product_detail', kwargs={'pk': product.pk})}?error={quote(message)}"
            return redirect(url)

        if not request.user.is_authenticated:
            return redirect_detail("Connectez-vous pour ajouter un article au panier.")

        try:
            qty = int(request.POST.get("quantity") or "1")
        except ValueError:
            qty = 1
        qty = max(1, qty)

        if product.stock < 1:
            return redirect_detail("Ce produit est en rupture de stock.")
        if qty > product.stock:
            return redirect_detail("Quantité supérieure au stock disponible.")

        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": qty},
        )
        if not created:
            new_qty = item.quantity + qty
            if new_qty > product.stock:
                return redirect_detail(
                    "Quantité totale dans le panier supérieure au stock disponible."
                )
            item.quantity = new_qty
            item.save()

        return redirect("cart_detail")


class CartDetailView(TemplateView):
	template_name = 'cart/cart_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		cart_items = []
		total_items = 0

		if self.request.user.is_authenticated:
			cart = getattr(self.request.user, 'cart', None)
			if cart is not None:
				cart_items = cart.items.select_related('product')
				total_items = sum(item.quantity for item in cart_items)

		context.update({
			'cart_items': cart_items,
			'total_items': total_items,
		})
		return context
