from django.shortcuts import render
from django.views import View
from .models import Product
from django.views.generic import DetailView, ListView


class ProductsListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'produits'


class ProductDetailsView(DetailView):
    template_name = "products/productDetail.html"
    model = Product
    context_object_name = 'product'
