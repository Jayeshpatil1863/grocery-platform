from django.shortcuts import get_object_or_404, render,redirect
from .models import Product,ProductForm
def add_product(request):
    if request.method=='POST':
        f=ProductForm(request.POST,request.FILES)
        f.save()
        return redirect("/dashboard/")
    else:
        return render(request,"addproduct.html",{'form':ProductForm})


def product_list(request):
    return render(request,"productlist.html",{'pl':Product.objects.all()})

def product_search(request):
    if request.method=='POST':
        pname=request.POST.get("search")
        return render(request,"searchproduct.html",{'pl':Product.objects.filter(name__contains=pname)})
    else:
        return render(request,"searchproduct.html",{'pl':Product.objects.all()})
    
def delete_product(request,id):
    p=Product.objects.get(id=id)
    p.delete()
    return redirect('product:list')

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product:list')
    else:
        form = ProductForm(instance=product)

    return render(request, "addproduct.html", {'form': form})
