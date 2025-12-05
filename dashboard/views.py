from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render

from orderapp.models import Order, OrderForm
from product.models import Product, ProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from account.models import ProductReview, UserProfile

def jayesh(request):
    p= Product.objects.all()
    con={'p':p}
    return render(request, 'jayesh.html',con)


def admin_home(request):

    # 1️⃣ सभी Products fetch + Pagination
    products = Product.objects.all().order_by('id')   # ORDER BY जोड़ दिया warning हटाने के लिए

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 2️⃣ Dashboard Counts
    total_products = Product.objects.count()
    total_users = UserProfile.objects.count()
    total_orders = Order.objects.count()

    print("----> Products List:", products)
    print("----> Admin Dashboard Accessed", total_users, total_products, total_orders)

    # 3️⃣ Context combine
    context = {
        'pl': page_obj,              # pagination वाली list
        'total_products': total_products,
        'total_users': total_users,
        'total_orders': total_orders,
    }

    return render(request, 'admin_home.html', context)




def admin_search(request):
    if request.method=='POST':
        pname=request.POST.get("search")
        return render(request,"admin_search.html",{'pl':Product.objects.filter(name__contains=pname)})
    else:
        return render(request,"admin_search.html",{'pl':Product.objects.all()})    


    

def admin_product_list(request):
    pl = Product.objects.select_related("user").all()  
    return render(request,"admin_productlist.html",{'pl':pl})

def admin_order_list(request):
    # Fetch all orders with related user and product in a single query
    orders = Order.objects.select_related('user').all()
    return render(request, 'admin_order_list.html', {'orders': orders})

def admin_order_edit(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard:orders')
    else:
        form = OrderForm(instance=order)
    return render(request, 'admin_order_edit.html', {'form': form, 'order': order})


def admin_order_delete(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('dashboard:orders')
    return render(request, 'admin_order_delete.html', {'order': order})

from django.core.paginator import Paginator


# def admin_homeeeee(request):
#     # सभी products fetch करो
#     products = Product.objects.all()

#     # Pagination setup – 8 products per page
#     paginator = Paginator(products, 8)  
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'admin_home.html', {'pl': page_obj})


def Products(request):
    pl = Product.objects.all()  # database से सभी products
    return render(request, 'products.html', {'pl': pl})

from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render

def Users(request):

    q = request.GET.get("q", "").strip()   # search value

    # If search text present → filter users
    if q:
        users = User.objects.filter(
            Q(username__icontains=q) |
            Q(email__icontains=q)
        ).order_by("-id")
    else:
        users = User.objects.all().order_by("-id")

    # Pagination
    paginator = Paginator(users, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "users.html", {
        "users": page_obj,     # LOOP me ye use hota hai
        "page_obj": page_obj,
    })


def user_delete(request, id):
    from django.contrib.auth.models import User
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('dashboard:users')
    return render(request, 'user_delete.html', {'user': user})


def user_edit(request, id):
    from django.contrib.auth.models import User
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        user.username = username
        user.email = email
        user.save()
        return redirect('dashboard:users')
    return render(request, 'user_edit.html', {'user': user})

def product_reviews(request):
    """
    Admin view: list product reviews with search and pagination.
    Search fields: user.username, product.name, comment, rating
    """
    q = request.GET.get('q', '').strip()
    reviews_qs = ProductReview.objects.select_related('product', 'user').all().order_by('-created_at')

    if q:
        # Try to match numeric rating query too if q is a number
        rating_filter = None
        if q.isdigit():
            rating_filter = Q(rating=int(q))

        reviews_qs = reviews_qs.filter(
            Q(user__username__icontains=q) |
            Q(product__name__icontains=q) |
            Q(comment__icontains=q) |
            (rating_filter if rating_filter is not None else Q())
        )

    # Pagination: 12 reviews per page (adjust as needed)
    paginator = Paginator(reviews_qs, 12)
    page = request.GET.get('page', 1)
    try:
        reviews_page = paginator.page(page)
    except PageNotAnInteger:
        reviews_page = paginator.page(1)
    except EmptyPage:
        reviews_page = paginator.page(paginator.num_pages)

    context = {
        'reviews': reviews_page,
        'q': q,  # pass current query to template so we can keep it in the search box & links
    }
    return render(request, 'product_reviews.html', context)

def delete_review(request, id):
    review = get_object_or_404(ProductReview, id=id)

    if request.method == "POST":
        review.delete()
        messages.success(request, "Review deleted successfully.")
        return redirect("dashboard:p_reviews")

    return redirect("dashboard:p_reviews")

def admin_product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "admin_product_detail.html", {'product': product})