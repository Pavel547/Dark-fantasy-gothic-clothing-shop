from django import forms
from .models import CartItem
from main.models import ProductSize


class AddToCartForm(forms.Form):
    size_id = forms.IntegerField(required=False, )
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
                    required=True,
                    error_messages={'required': 'Please select size'})
                
        
    def clean_size(self):
        size_id = self.cleaned_data.get('size_id')
        product = self.product
        
        if not size_id:
            raise forms.ValidationError('Please select size')
        
        product_size = ProductSize.objects.filter(
            product=product, id=size_id, in_stock__gt=0).exists()
        
        if not product_size:
            raise forms.ValidationError('Size not availible now')           
        
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
