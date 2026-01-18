from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from django.views.generic import View
from django.template.response import TemplateResponse
from .models import Cart, CartItem
from .forms import UpdateCartItem, AddToCartForm
from main.models import Product, ProductSize
from django.db import transaction
import json


class CartMixin:
    def get_cart(self, request):
        if hasattr(request, 'cart'):
            return request.session.cart
        
        if request.session.session_key:
            return request.session.create()
        
        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key
        )
        
        request.session['cart_id'] = cart.id
        request.session.modified = True
        
        return cart
    
    
class CartPageView(CartMixin, View):
    def get(self, request):
        cart = self.get_cart(request)
        
        context = {
            'total_price': cart.subtotal,
            'cart_items': cart.items.select_related(
                'product', 'product_size__size').order_by('-created_at')
        }
        
        return redirect(request, 'cart/cart.html', context)
    

class AddToCartView(CartMixin, View):
    def post(self, request, slug):
        cart = self.get_cart(request)
        product = get_object_or_404(Product, slug=slug) 
        
        form = AddToCartForm(request.POST, product)
        
        if not form.is_valid():
            return JsonResponse({
                'error': 'Invalid form data',
                'form_errors': form.errors,
            }, status=400)
        
        size_id = form.cleaned_data.get('size_id')
        if size_id:
            product_size = get_object_or_404(ProductSize, id=size_id,
                                             product=product)
        else:
            product_size = product.product_size.filter(
                stock__gt=0).first()
            if not product_size:
                return JsonResponse({
                    'error': 'No avalible sizes now'
                }, status=400)
                
        quantity = form.cleaned_data.get('quantity')
        if quantity > product_size.stock:
            return JsonResponse({
                'error': f'Only {product_size.stock} avalible now'
            }, status=400)
            
        existing_item = cart.items.filter(
            product=product, product_size=product_size).first()
        if existing_item:
            total_item = existing_item.quantity + quantity
            if total_item.quantity > product_size.stock:
                return JsonResponse({
                    'error': f"""Cannot add {total_item.quantity}. 
                    Only {product_size.stock - existing_item.quantity} avalible now."""
                }, status=400)
                
        cart_item = cart.add_item(product, product_size, quantity)
                
        request.session['cart_id'] = cart.id
        request.session.modified = True
        
        return redirect('cart:cart_page')
        