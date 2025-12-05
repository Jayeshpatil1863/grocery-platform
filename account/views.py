from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from product.models import Product
from django.contrib.auth import  login,logout,authenticate
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    # सभी products fetch करो
    products = Product.objects.all()
    print('----> Products Fetched:', products)

    # Pagination setup – 8 products per page
    paginator = Paginator(products, 8)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'pl': page_obj})

from .models import CustomUserCreationForm, ProductReview, UserProfile

def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()   # normal user create

            role = request.POST.get("role")  # form se role nikala
            UserProfile.objects.create(user=user, role=role)  # profile banayi

            return redirect('account:login')
    else:
        form = CustomUserCreationForm()

    return render(request, "adduser.html", {'form': form})

# def login_user(request):
#     if request.method == 'POST':
#         uname = request.POST.get("uname")
#         passw = request.POST.get("passw")

#         user = authenticate(request, username=uname, password=passw)

#         if user is not None:
#             login(request, user)

#             # --- IMPORTANT ---
#             # If admin → admin dashboard
#             # If normal user → homepage
#             if hasattr(user, 'role') and user.role == 'admin':
#                 return redirect('/admin/dashboard/')
#             else:
#                 return redirect('/')

#         else:
#             messages.error(request, "Invalid Username or Password")
#             return render(request, 'login.html')

#     return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from account.models import UserProfile   # <-- import your profile model

def login_user(request):
    if request.method == 'POST':
        uname = request.POST.get("uname")
        passw = request.POST.get("passw")

        user = authenticate(request, username=uname, password=passw)

        if user is not None:
            login(request, user)

            # ---- Fetch UserProfile role ----
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                messages.error(request, "User Profile not found!")
                return redirect('/login/')

            # ---- Redirect based on role ----
            if profile.role == "admin":
                return redirect('/dashboard/')
            else:
                return redirect('/')   # normal user home page

        else:
            messages.error(request, "Invalid Username or Password")
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect("/")

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    # Paginate reviews: 5 per page
    reviews_qs = product.reviews.all().order_by('-created_at')  # newest first
    paginator = Paginator(reviews_qs, 5)
    page_number = request.GET.get('page', 1)

    try:
        reviews_page = paginator.page(page_number)
    except PageNotAnInteger:
        reviews_page = paginator.page(1)
    except EmptyPage:
        reviews_page = paginator.page(paginator.num_pages)

    context = {
        'product': product,
        'reviews_page': reviews_page,
    }
    return render(request, "product_detail.html", context)


def add_review(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "").strip()

        # Validation
        try:
            rating = int(rating)
        except (TypeError, ValueError):
            messages.error(request, "Invalid rating.")
            return redirect("account:detail", id=id)

        if not (1 <= rating <= 5):
            messages.error(request, "Rating must be between 1 and 5.")
            return redirect("account:detail", id=id)

        if comment == "":
            messages.error(request, "Please write a review.")
            return redirect("account:detail", id=id)

        # create or update user's review
        existing = ProductReview.objects.filter(product=product, user=request.user).first()
        if existing:
            existing.rating = rating
            existing.comment = comment
            existing.save()
            messages.success(request, "Your review was updated.")
        else:
            ProductReview.objects.create(product=product, user=request.user, rating=rating, comment=comment)
            messages.success(request, "Review submitted. Thank you!")

        # after save, compute last page so user sees the newly added review
        all_count = product.reviews.count()
        per_page = 5
        last_page = (all_count // per_page) + (1 if all_count % per_page else 0)
        detail_url = reverse("account:detail", args=[id])
        return redirect(f"{detail_url}?page={last_page}")

    # For GET requests, go back to detail page
    return redirect("account:detail", id=id)


def delete_review(request, review_id):
    review = get_object_or_404(ProductReview, id=review_id)
    # Only POST allowed for deletion
    if request.method != "POST":
        return redirect("account:detail", id=review.product.id)

    if review.user != request.user:
        messages.error(request, "You cannot delete this review.")
        return redirect("account:detail", id=review.product.id)

    product_id = review.product.id
    review.delete()
    messages.success(request, "Review deleted.")
    return redirect("account:detail", id=product_id)

