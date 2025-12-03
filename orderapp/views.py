from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from product.models import Product
from .models import Address, AddressForm, OrderForm, Order
from cart.models import Cart

# ✅ CREATE (Place Order)
@login_required
def place_order(request):
    cart_items = Cart.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            for item in cart_items:
                Order.objects.create(
                    user=request.user,
                    product=item.product,
                    quantity=item.quantity,
                    total_price=item.price * item.quantity,
                    delivery_slot=form.cleaned_data['delivery_slot']
                )
            cart_items.delete()  # Clear cart after order
            return render(request, "order_success.html")
    else:
        form = OrderForm()
    return render(request, "place_order.html", {'form': form, 'cart_items': cart_items})

# ✅ READ (User view orders)
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "my_orders.html", {'orders': orders})

# ✅ READ (Admin view all orders)
@login_required
def all_orders(request):
    if not request.user.is_staff:
        return redirect('/')
    orders = Order.objects.all()
    return render(request, "all_orders.html", {'orders': orders})

# ✅ UPDATE (Admin can update status)
@login_required
def update_order_status(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        return redirect('order:all_orders')
    return render(request, "update_status.html", {'order': order})

# ✅ DELETE (Admin cancel/delete order)
@login_required
def delete_order(request, id):
    order = get_object_or_404(Order, id=id)
    order.delete()
    return redirect('order:all_orders')
from django.shortcuts import render

from django.contrib import messages

def order_success(request):
    order_ids = request.session.get("recent_orders", [])

    orders = Order.objects.filter(id__in=order_ids)

    # Clear session so repeat refresh se dikh na aaye
    request.session["recent_orders"] = []

    return render(request, "success.html", {"orders": orders})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order, Address
from .models import OrderForm, AddressForm
from cart.models import Cart  # jaha se cart items aa rahe hain

# def checkout_view(request):
#     user = request.user

#     cart_items = Cart.objects.filter(user=user)
#     total = sum(item.price * item.quantity for item in cart_items)

#     addresses = Address.objects.filter(user=user)

#     order_form = OrderForm()
#     address_form = AddressForm()

#     if request.method == "POST":
#         order_form = OrderForm(request.POST)

#         # NEW or OLD address?
#         add_new = request.POST.get("add_new_address")

#         # ------------------------------
#         # 1. HANDLE ADDRESS
#         # ------------------------------
#         if add_new == "yes":
#             address_form = AddressForm(request.POST)
#             if address_form.is_valid():
#                 address = address_form.save(commit=False)
#                 address.user = user
#                 address.save()
#             else:
#                 messages.error(request, "Please enter valid address!")
#                 return redirect("order:checkout")
#         else:
#             # OLD ADDRESS SELECTED
#             address_id = request.POST.get("selected_address")
#             address = Address.objects.get(id=address_id, user=user)

#             # ⭐⭐⭐ MAKE SELECTED ADDRESS DEFAULT ⭐⭐⭐
#             Address.objects.filter(user=user, is_default=True).update(is_default=False)
#             address.is_default = True
#             address.save()

#         # ------------------------------
#         # 2. CREATE ORDER + Reduce Stock
#         # ------------------------------
#         if order_form.is_valid():
#             delivery_slot = order_form.cleaned_data["delivery_slot"]
            
#             for item in cart_items:

#                 product = item.product  # Cart ka product
                
#                 # ***** Reduce Stock *****
#                 if product.stock >= item.quantity:
#                     product.stock -= item.quantity
#                     product.save()
#                 else:
#                     messages.error(request, f"'{product.name}' ka stock kam pad gaya!")
#                     return redirect("order:checkout")

#                 # ***** CREATE ORDER *****
#                 Order.objects.create(
#                     user=user,
#                     product=product,
#                     quantity=item.quantity,
#                     total_price=item.price * item.quantity,
#                     delivery_slot=delivery_slot,
#                     address=address
#                 )

#                 # clear cart after order
#             Cart.objects.filter(user=user).delete()

#             return redirect("order:success")

#     context = {
#         "addresses": addresses,
#         "order_form": order_form,
#         "address_form": address_form,
#         "total": total
#     }

#     return render(request, "checkout.html", context)


# views.py
from django.db import transaction  # <-- Yeh import karein
from django.shortcuts import render, redirect
from django.contrib import messages
# (Aapke baaki imports)

# def checkout_view(request):
#     user = request.user
#     cart_items = Cart.objects.filter(user=user)
    
#     # Agar cart khaali hai toh checkout page pe nahi rehna chahiye
#     if not cart_items.exists():
#         messages.warning(request, "Aapka cart khaali hai.")
#         return redirect("cart_app:cart_view") # Cart page pe bhej do

#     total = sum(item.price * item.quantity for item in cart_items)
#     addresses = Address.objects.filter(user=user)
#     order_form = OrderForm()
#     address_form = AddressForm()

#     if request.method == "POST":
#         order_form = OrderForm(request.POST)

#         # ------------------------------
#         # 1. HANDLE ADDRESS
#         # ------------------------------
#         add_new = request.POST.get("add_new_address")
#         address = None # Address ko pehle define kar lein

#         if add_new == "yes":
#             address_form = AddressForm(request.POST)
#             if address_form.is_valid():
#                 address = address_form.save(commit=False)
#                 address.user = user
#                 address.save()
#             else:
#                 messages.error(request, "Please enter valid address!")
#                 return redirect("order:checkout")
#         else:
#             address_id = request.POST.get("selected_address")
#             if not address_id:
#                 messages.error(request, "Please select a delivery address.")
#                 return redirect("order:checkout")
                
#             try:
#                 address = Address.objects.get(id=address_id, user=user)
#                 # Optional: Make selected address default
#                 Address.objects.filter(user=user, is_default=True).update(is_default=False)
#                 address.is_default = True
#                 address.save()
#             except Address.DoesNotExist:
#                 messages.error(request, "Invalid address selected.")
#                 return redirect("order:checkout")

#         # ------------------------------
#         # 2. CREATE ORDER (Transaction ke saath)
#         # ------------------------------
#         if order_form.is_valid() and address:
#             delivery_slot = order_form.cleaned_data["delivery_slot"]

#             try:
#                 # Yahan se transaction shuru hota hai
#                 with transaction.atomic():
                    
#                     # ----- STEP 1: Pehle sabka stock check karo -----
#                     for item in cart_items:
#                         product = item.product
#                         if product.stock < item.quantity:
#                             # Agar ek ka bhi stock kam hai, toh poora order cancel kardo
#                             messages.error(request, f"'{product.name}' ka stock kam pad gaya! Order nahi hua.")
#                             # transaction.atomic() poora process automatically reverse kar dega
#                             return redirect("order:checkout")

#                     # ----- STEP 2: Agar sab stock mein hai, tab order create karo -----
#                     for item in cart_items:
#                         product = item.product
                        
#                         # Stock reduce karo
#                         product.stock -= item.quantity
#                         product.save()

#                         # Order create karo
#                         o= Order.objects.create(
#                             user=user,
#                             product_name=item.product,
#                             image=item.image if item.image else None,
#                             quantity=item.quantity if item.quantity else 1,
#                             total_price=item.price * item.quantity,
#                             delivery_slot=delivery_slot,
#                             address=address
#                         )
#                         o.save()
#                     # Cart clear karo


#                     u = Cart.objects.filter(user=request.user) # cart_items ek queryset hai, seedha .delete() kar sakte hain
#                     u.delete()
                    
#                     # ----- STEP 3: Loop ke BAHAR cart delete karo -----
                    

#             except Exception as e:
#                 # Agar koi aur galti hoti hai
#                 messages.error(request, f"Ek error aa gaya: {e}")
#                 return redirect("order:checkout")

#             # ----- STEP 4: Transaction safal hone par redirect karo -----
#             return redirect("order:success")

#     # Yeh context 'GET' request ke liye aur 'POST' fail hone par kaam aayega
#     context = {
#         "addresses": addresses,
#         "order_form": order_form,
#         "address_form": address_form,
#         "total": total
#     }
#     return render(request, "checkout.html", context)


def checkout_view(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        messages.warning(request, "Aapka cart khaali hai.")
        return redirect("cart:viewcart")

    total = sum(item.price * item.quantity for item in cart_items)

    addresses = Address.objects.filter(user=user)
    order_form = OrderForm()
    address_form = AddressForm()

    if request.method == "POST":

        print("POST RECEIVED")  # DEBUG

        order_form = OrderForm(request.POST)

        print("FORM VALID:", order_form.is_valid())  # DEBUG
        print(order_form.errors)                    # DEBUG

        add_new = request.POST.get("add_new_address")
        address = None

        # ----------------------
        # Address handle
        # ----------------------
        if add_new == "yes":
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user = user
                address.save()
        else:
            address_id = request.POST.get("selected_address")
            address = Address.objects.get(id=address_id, user=user)

        # ----------------------
        # Order create
        # ----------------------
        if order_form.is_valid():
            delivery_slot = order_form.cleaned_data["delivery_slot"]

            for item in cart_items:

                print("Saving Order For:", item.product)   # DEBUG

                Order.objects.create(
                    user=user,
                    image=item.image,
                    product_name=item.name,
                    quantity=item.quantity,
                    total_price=item.price * item.quantity,
                    delivery_slot=delivery_slot,
                    address=address
                )

            print("Order Saved Successfully!")  # DEBUG

            cart_items.delete()

            return redirect("orderapp:success")

    context = {
        "addresses": addresses,
        "order_form": order_form,
        "address_form": address_form,
        "total": total
    }
    return render(request, "checkout.html", context)
