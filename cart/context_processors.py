from .models import Cart

def cart_context(request):    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user
        )
        
        context = {
            'total_items': cart.total_items,
        }
        
        return context
    else:
        if not request.session.session_key:
            request.session.create()
        
        cart, created = Cart.objects.get_or_create(
            session_key=request.session.session_key,
        )
        
        context = {
            'total_items': cart.total_items,
        }
        
        return context
        