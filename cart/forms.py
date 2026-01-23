from django import forms
from .models import CartItem
from main.models import ProductSize


class AddToCartForm(forms.Form):
    size_id = forms.IntegerField(required=False)
    quantity  = forms.IntegerField(min_value=1, initial=1)
    
    def __init__(self, *args, product=None,**kwargs):
        super().__init__(*args, **kwargs)
        self.product = product
        
        if product:
            sizes = product.product_sizes.filter(stock__gt=0)
            if sizes:
                self.fields['size_id'] = forms.ChoiceField(
                    choices=[(ps.id, ps.size.name) for ps in sizes],
                    initial=sizes.first().id,
                    required=True)
                
        
    def clean_size(self, product=None):
        size_id = self.cleaned_data["size_id"]
        self.product = product
        
        product_size = ProductSize.objects.filter(
            product=product,
            id=size_id,
            stock__gt=0
        ).exists()
        if not product_size:
            raise forms.ValidationError('Size does not exists')
        
        return size_id
    

class UpdateCartItem(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.product_sizes:
            self.fields['quantity'].append(
                forms.validators.MaxValueValidator(self.product_sizes.stock)
            )
