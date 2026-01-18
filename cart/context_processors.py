from .models import Cart

def cart_context(request):
    if not request.session.session_key:
        request.session.create()
        
    cart, created = Cart.objects.get_or_create(
        session_key=request.session.session_key
    )

    context = {
        'cart_total_items': cart.total_items,
        'cart_subtotal': cart.subtotal,
    }

    return context