from .models import Cart

def cart_count(request):
    # Session se cart count nikalo
    count = request.session.get('cart_count', 0)
    return {'cart_count': count}
