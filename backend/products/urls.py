from django.urls import path

from .views import ProductDetailsView, ProductsListView

urlpatterns = [
    path('', ProductsListView.as_view(), name='products_list'),
    path('<int:pk>/', ProductDetailsView.as_view(), name='product_detail'),
]