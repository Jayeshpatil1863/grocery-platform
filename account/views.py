from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm
from product.models import Product
from django.contrib.auth import  login,logout,authenticate
from django.core.paginator import Paginator

def home(request):
    # सभी products fetch करो
    products = Product.objects.all()
    print('----> Products Fetched:', products)

    # Pagination setup – 8 products per page
    paginator = Paginator(products, 8)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'pl': page_obj})

from .models import CustomUserCreationForm, UserProfile

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
    return render(request, "product_detail.html", {"product": product})