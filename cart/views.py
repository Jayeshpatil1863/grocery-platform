from operator import mul
from django.shortcuts import get_object_or_404, redirect, render

from product.models import Product
from .models import Cart,CartForm

def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    # Check if product already in cart
    cart_item, created = Cart.objects.get_or_create(
        product=product,
        user=request.user,
        defaults={
            'name': product.name,
            'image': product.pimg,
            'price': product.price,
            'quantity': 1
        }
    )

    # If already exists, increase quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return render(request, "addtocart.html", {
        'msg': f"{product.name} added to cart successfully ✅"
    })



def view_cart(request):
    u = Cart.objects.filter(user=request.user)
    for item in u:
        item.total_price = item.price * item.quantity
    total = sum(item.total_price for item in u)

    # 👇 Cart seen hone ke baad reset kar do
    request.session['cart_count'] = 0

    return render(request, "cartlist.html", {'cl': u, 'total': total})



# ✅ Quantity increase view
def increase_quantity(request, id):
    item = get_object_or_404(Cart, id=id)
    item.quantity += 1
    item.save()
    return redirect('cart:viewcart')


# ✅ Quantity decrease view
def decrease_quantity(request, id):
    item = get_object_or_404(Cart, id=id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()  # quantity 0 hone pe item remove kar do
    return redirect('cart:viewcart')


def delete_item(request, id):
    item = get_object_or_404(Cart, id=id)
    item.delete()
    return redirect('cart:viewcart')