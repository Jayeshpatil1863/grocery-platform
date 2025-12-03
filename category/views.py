from django.shortcuts import render,redirect
from .models import Category,CategoryForm

def add_category(request):
    if request.method=='POST':
        f=CategoryForm(request.POST)
        f.save()
        return redirect("/")
    else:
        return render(request,'addcategory.html',{'form':CategoryForm})
 

def category_list(request):
    return render(request,"categorylist.html",{'cl':Category.objects.all()})