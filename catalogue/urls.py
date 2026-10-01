from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('produit/<slug:slug>/', views.product_detail, name='product_detail'),
    path('categorie/<slug:slug>/', views.category_detail, name='category_detail'),
    path('panier/', views.cart_detail, name='cart_detail'),
    path('panier/ajouter/<int:product_id>/', views.cart_add, name='cart_add'),
    path('panier/retirer/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('commande/paiement/', views.create_checkout_session, name='checkout'),
    path('commande/succes/', views.order_success, name='order_success'),
]