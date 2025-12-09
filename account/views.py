from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from e_com.settings import EMAIL_HOST_USER
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

from django.db.models import Avg

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    reviews_qs = product.reviews.all().order_by('-created_at')

    paginator = Paginator(reviews_qs, 5)
    page_number = request.GET.get('page', 1)

    try:
        reviews_page = paginator.page(page_number)
    except PageNotAnInteger:
        reviews_page = paginator.page(1)
    except EmptyPage:
        reviews_page = paginator.page(paginator.num_pages)

    avg_rating = reviews_qs.aggregate(avg=Avg('rating'))['avg']

    context = {
        'product': product,
        'reviews_page': reviews_page,
        'avg_rating': avg_rating,
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


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
import random
from django.core.mail import send_mail

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)

            request.session['reset_email'] = email
            request.session['reset_otp'] = otp

            send_mail(
                "Password Reset OTP",
                f"Your OTP is: {otp}",
                EMAIL_HOST_USER, 
                [email],
                fail_silently=False,
            )

            messages.success(request, "OTP sent to your email")
            return redirect('account:verify_otp')

        except User.DoesNotExist:
            messages.error(request, "Email not registered")

    return render(request, "forgot_password.html")


def verify_otp(request):
    # agar direct yaha aaye bina email dale, to redirect
    if 'reset_otp' not in request.session:
        messages.error(request, "Session expired, please try again.")
        return redirect('account:forgot_password')

    if request.method == "POST":
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('reset_otp')

        if user_otp == str(session_otp):
            messages.success(request, "OTP Verified")
            return redirect('account:reset_password')
        else:
            messages.error(request, "Invalid OTP")

    return render(request, "verify_otp.html")


def reset_password(request):
    if 'reset_email' not in request.session:
        messages.error(request, "Session expired, please try again.")
        return redirect('account:forgot_password')

    if request.method == "POST":
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('account:reset_password')

        email = request.session.get('reset_email')

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            # session clean
            request.session.pop('reset_otp', None)
            request.session.pop('reset_email', None)

            messages.success(request, "Password reset successfully")
            return redirect('account:login')

        except User.DoesNotExist:
            messages.error(request, "User not found, try again.")
            return redirect('account:forgot_password')

    return render(request, "reset_password.html")
