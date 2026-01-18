from django import forms
from .models import CartItem


class AddToCartForm(forms.Form):
    size_id = forms.IntegerField(required=False)
    quantity  = forms.IntegerField(min_value=1, initial=1)
    
    
    def __init__(self, *args, product=None,**kwargs):
        super().__init__(*args, **kwargs)
        self.product = product
        
        if product:
            sizes = product.product_size.filter(stock__gt=0)
            if sizes:
                self.fields['size_id'] = forms.ChoiceField(
                    choices=[(ps.name, ps.id) for ps in sizes],
                    initial=sizes.first().id,
                    required=True)
                

class UpdateCartItem(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.product_size:
            self.fields['quantity'].append(
                forms.validators.MaxValueValidator(self.product_size.stock)
            )
