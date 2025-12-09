from django.shortcuts import get_object_or_404, render,redirect
from .models import Product,ProductForm, ProductImage


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)

            images = request.FILES.getlist('images')

            if images:
                # ✅ First image = main image
                product.pimg = images[0]

            product.save()

            # ✅ Baaki images = extra gallery images
            for img in images[1:]:
                ProductImage.objects.create(product=product, image=img)

            return redirect("/dashboard/")
    else:
        form = ProductForm()

    return render(request, "addproduct.html", {'form': form})


def product_list(request):
    return render(request,"productlist.html",{'pl':Product.objects.all()})

def product_search(request):
    if request.method=='POST':
        pname=request.POST.get("search")
        return render(request,"searchproduct.html",{'pl':Product.objects.filter(name__contains=pname)})
    else:
        return render(request,"searchproduct.html",{'pl':Product.objects.all()})
    
def delete_product(request, id):
    p = get_object_or_404(Product, id=id)
    p.delete()
    return redirect("/dashboard/")

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        images = request.FILES.getlist('images')   # ✅ multiple images

        if form.is_valid():
            product = form.save(commit=False)

            # ✅ Agar nayi images aayi hain to:
            if images:
                # First image ko main image bana do
                product.pimg = images[0]

            product.save()

            # ✅ Baaki images ko extra gallery me add karo
            for img in images[1:]:
                ProductImage.objects.create(product=product, image=img)

            return redirect('product:list')

    else:
        form = ProductForm(instance=product)

    return render(request, "addproduct.html", {
        'form': form,
        'product': product
    })

