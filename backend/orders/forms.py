from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("shipping_address",)
        widgets = {
            "shipping_address": forms.Textarea(
                attrs={"rows": 4, "class": "form-control", "placeholder": "Adresse de livraison complète"}
            ),
        }
