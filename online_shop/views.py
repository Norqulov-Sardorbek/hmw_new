from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from online_shop.models import Category, Product, Comment
from online_shop.forms import OrderModelForm, ProductModelForm

def home(request, category: int | None = None) -> None:
    products = Product.objects.filter(category=category) if category else Product.objects.all()
    query = request.GET.get("query")
    categories = Category.objects.all()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    for product in products:
        product.rating_range = range(product.rating)
    return render(request, 'online_shop/home.html', {'products': products, "categories": categories})



def details(request, product_id: int) -> None:
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(owner=product).order_by('-commented_date')
    recently_viewed = request.session.get("recently_viewed", [])
    if product_id in recently_viewed:
        recently_viewed.remove(product_id)
    recently_viewed.insert(0, product_id)
    recently_viewed = recently_viewed[:5]
    request.session["recently_viewed"] = recently_viewed
    products = Product.objects.filter(id__in=recently_viewed).exclude(id=product.id)
    return render(request, 'online_shop/detail.html', {'product': product, 'comments': comments, 'products': products})

def comment(request, product_id: int) -> None:
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        Comment.objects.create(name=request.POST.get("name"), comment=request.POST.get("comment"), owner=product)
        return redirect("product_details", product_id=product_id)
    return redirect("product_details", product_id=product_id)

def filter(request, command: str) -> None:
    products = Product.objects.all().order_by(command)
    categories = Category.objects.all()
    for product in products:
        product.rating_range = range(product.rating)
    return render(request, 'online_shop/home.html', {"categories": categories, 'products': products})

def admin(request) -> None:
    form = ProductModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(commit=False)
        return redirect('home')
    return render(request, 'online_shop/admin-page.html', {'form': form})

def edit_object(request, product_id: int) -> None:
    obj = get_object_or_404(Product, id=product_id)
    form = ProductModelForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'online_shop/admin-page.html', {'form': form})

def delete_product(request, product_id: int) -> None:
    obj = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        obj.delete()
        return redirect('home')
    return render(request, 'online_shop/confirm-delete.html', {'product': obj})

def order_view(request, pk: int) -> None:
    product = Product.objects.get(id=pk)
    form = OrderModelForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        quantity = int(request.POST.get('quantity'))
        if product.quantity >= quantity:
            order = form.save(commit=False)
            order.product = product
            product.quantity -= quantity
            product.save()
            order.save()
            messages.success(request, 'Order successfully created')
            return redirect('product_details', product.id)
        messages.error(request, 'Something is wrong')
    return render(request, 'online_shop/detail.html', {'form': form, 'product': product})