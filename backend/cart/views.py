from django.views.generic import TemplateView


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
