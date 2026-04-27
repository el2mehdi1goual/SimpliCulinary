from django.shortcuts import render
from django.views import View
from .models import Product
# Create your views here.
class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'products/product_list.html', {'products': products})
