from django.contrib import admin
from .models import Category, Product, Size, \
    ProductSize, Material, ProductMaterial

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 0
    
class ProductMaterialInline(admin.TabularInline):
    model = ProductMaterial
    extra = 0
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price', 'color')
    list_filter = ('category', 'color')
    search_fields = ('name', 'category')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSizeInline, ProductMaterialInline]
    

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', )
