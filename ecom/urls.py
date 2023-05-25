from django.urls import path
from .views import *

urlpatterns = [
    path('homepage',Product_page.as_view(method_name = 'homepage'),name = 'homepage'),
    path('cart',Product_page.as_view(method_name = 'show_cart'),name = 'cart'),
    path('update_quantity',Product_page.as_view(method_name = 'update_quantity'),name = 'update_quantity'),
    path('update_cart',Product_page.as_view(method_name = 'update_cart'),name = 'update_cart'),
    path('remove_cart/<slug:slug>',Product_page.as_view(method_name = 'remove_cart'),name = 'remove_cart'),

    path('list_products',Product_crud.as_view(method_name = 'list_products'),name = 'list_products'),
    path('add_product',Product_crud.as_view(method_name = 'add_product'),name = 'add_product'),
    path('add_product',Product_crud.as_view(method_name = 'add_product'),name = 'add_product'),
    path('edit/<slug:slug>',Product_crud.as_view(method_name = 'edit_product'),name = 'edit_product'),
    path('delete_product',Product_crud.as_view(method_name = 'delete_product'),name = 'delete_product'),

]