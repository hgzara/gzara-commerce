import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .cart import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY


def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'catalogue/product_list.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalogue/product_detail.html', {'product': product})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'catalogue/category_detail.html', {'category': category, 'products': products})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'catalogue/cart_detail.html', {'cart': cart})


def create_checkout_session(request):
    cart = Cart(request)
    line_items = []
    for item in cart:
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': item['product'].name},
                'unit_amount': int(item['price'] * 100),
            },
            'quantity': item['quantity'],
        })

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/commande/succes/'),
        cancel_url=request.build_absolute_uri('/panier/'),
    )
    return redirect(checkout_session.url, code=303)


def order_success(request):
    cart = Cart(request)
    cart.session['cart'] = {}
    cart.save()
    return render(request, 'catalogue/order_success.html')