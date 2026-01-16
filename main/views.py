from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from django.template.response import TemplateResponse
from .models import Category, Product, Size


class IndexView(TemplateView):
    template_name = 'base.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.headers.get('HX-Request'):
            return TemplateResponse(request, 'main/home.html', context)
        return TemplateResponse(request, self.template_name, context)
    
    
class CatalogView(ListView):
    template_name = 'main/catalog.html'
    model = Product
    context_object_name = 'products'
    
    # Filtration functions for get_queryset method
    FILTER_FUNCRIONS = {
        'min_price': lambda queryset, value: queryset.filter(price__gte=value),
        'max_price': lambda queryset, value: queryset.filter(price__lte=value), 
        'color': lambda queryset, value: queryset.filter(color__iexact=value), 
        'size': lambda queryset, value: queryset.filter(product_size__size__name=value), 
        'on_stock': lambda queryset, value: queryset.filter(product_size__on_stock=value),
    }
    
    def get_queryset(self):
        qs = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        
        if category_slug:
            current_category = Category.objects.filter(slug=category_slug)
            qs = qs.filter(category=current_category)            
        
        for params, filter_func in self.FILTER_FUNCRIONS.items():
            value = self.request.GET.get(params)
            if value:
                qs = filter_func(qs, value)
            else:
                qs = ''
        return qs
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['sizes'] = Size.objects.all()
        
        for param in self.FILTER_FUNCRIONS.keys():
            value = self.request.GET.get(param)
            if value:
                context[param] = value
            else:
                context[param] = ''
                
        return context
        

class ProductDetails(DetailView):
    model = Product
    template_name = 'main/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['current_category'] = product.category.slug
        context['similar_products'] = Product.objects.filter(
            category=product.category).exclude(id=product.id)[:4]
        return context
