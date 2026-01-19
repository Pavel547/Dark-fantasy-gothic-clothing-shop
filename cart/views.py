from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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
        
        if not request.session.session_key:
            return request.session.create()
        
        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key
        )
        
        return cart
    
    
class CartDetailView(CartMixin, View):
    def get(self, request):
        cart = self.get_cart(request)
        
        context = {
            'cart': cart,
            'cart_items': cart.items.select_related(
                'product', 'product_size__size').order_by('-added_at')
        }
        
        return TemplateResponse(request, 'cart/cart.html', context)
    

class AddToCartView(CartMixin, View):
    @transaction.atomic
    def post(self, request, slug):
        cart = self.get_cart(request)
        product = get_object_or_404(Product, slug=slug)
        
        form = AddToCartForm(request.POST, product=product)
        
        if not form.is_valid():
            messages.error(request, f'Invalid data {form.errors}.')

        size_id = form.cleaned_data.get('size_id')
        if size_id:
            product_size = get_object_or_404(
                ProductSize,
                product=product,
                id=size_id
            )
        else:
            product_size = product.product_sizes.filter(stock__gt=0).first()
            if not product_size:
                messages.info(request, 'No sizes avalible now.')
        
        quantity = form.cleaned_data.get('quantity')
        if quantity > product.product_sizes.stock:
            messages.info(request, 
                          f'Only {product.product_sizes.stock} avalible now')
            
        existing_item = get_object_or_404(CartItem, cart=cart, product=product)
        if existing_item:
            total_quantity = existing_item.quantity + quantity
            if total_quantity > product.product_sizes.stock:
                message = f"""Cannot add {total_quantity} items. 
                Only {product.product_sizes.stock} avalible."""
                messages.info(request, message=message)
                
        cart_item = cart.add_item(product, product_size, quantity)
        
        message.info(request, f'{product.name} succesfully add to cart')
        
        return redirect('cart:details')
        
        
class UpdateCartItemView(CartMixin, View):
    @transaction.atomic
    def post(self, request, item_id):
        cart = self.get_cart(request)
        cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
        
        quantity = request.POST.get('quantity', 1)
        
        if quantity < 0:
            messages.error(request, 'Invalid quantity')
            
        if quantity == 0:
            cart_item.delete()
        else:
            if quantity > cart_item.product_size.stock:
                messages.error(request, 
                               f'Only {cart_item.product_size.stock} avalible now')
            cart_item.quantity = quantity
            cart_item.save()
        
        context = {
            'cart': cart,
            'cart_items': cart.items.select_related(
                'prodcut', 'product_size__size').order_by('-added_at')
        }
        
        return TemplateResponse(request, 'cart/cart.html', context)
    
    
class DeleteCartItemView(CartMixin, View):
    def post(self, request, item_id):
        cart = self.get_cart(request)
        
        try:
            cart_item = get_object_or_404(CartItem, cart=cart, id=item_id)
            cart_item.delete()
            
            context = {
                'cart': cart,
                'cart_items': cart.items.select_related(
                    'product', 'product_size__size').order_by('-added_at')
            }
            
            return TemplateResponse(request, 'cart/cart.html', context)
        except CartItem.DoesNotExist:
            messages.error(request, 'Item not found')
            

class ClearCartView(CartMixin, View):
    def post(self, request):
        cart = self.get_cart(request)
        cart.clear()
        
        messages.info(request, 'Cart successfully cleared')
        return TemplateResponse(request, 'cart/cart.html', {'cart': cart})
