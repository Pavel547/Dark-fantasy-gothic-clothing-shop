from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    
    def save(self, *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.name} - {self.slug}'
    

class Material(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.name}'
    
    
class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)
        
    def __str__(self):
        return f'{self.name}'
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    main_image = models.ImageField(upload_to='media/product/main-image')
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'{self.name}'
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
        
class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_sizes')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    on_stock = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.size.name} ({self.stock} in stock for {self.product.name})"
    
    
    def save(self, *args, **kwargs):
        if self.stock > 0:
            self.on_stock = True
        else:
            self.on_stock = False
        super().save(*args, **kwargs)
        
        
class ProductMaterial(models.Model):
    prodct = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    percentage = models.PositiveIntegerField()
    
    def __str__(self):
        return f'{self.prodct.name} - {self.material.name} ({self.percentage}%)'
