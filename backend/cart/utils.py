"""Utilitaires pour le panier (utilisateur connecté ou session invité)."""

from .models import Cart


def get_cart(request):
    """
    Retourne le panier associé à la requête : compte utilisateur ou clé de session.
    Crée le panier et, pour un invité, la session si nécessaire.
    """
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    if not request.session.session_key:
        request.session.create()

    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart
