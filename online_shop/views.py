from django.db.models import Q
from .forms import ProductModelForm
from online_shop.models import Category


# Create your views here.

def home(request, category: int | None = None):
    if category:
        products = Product.objects.all().filter(category=category)
    else:
        products = Product.objects.all()
    query = request.GET.get("query")
    categories = Category.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    for product in products:
        product.rating_range = range(product.rating)
    context = {
        'products': products,
        "categories": categories,

    }
    return render(request, 'online_shop/home.html', context=context)


def details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(owner=product).order_by('-commented_date')
    recently_viewed = request.session.get("recently_viewed", [])

    if product_id in recently_viewed:
        recently_viewed.remove(product_id)
    recently_viewed.insert(0, product_id)
    recently_viewed = recently_viewed[:5]
    request.session["recently_viewed"] = recently_viewed
    products = Product.objects.filter(id__in=recently_viewed).exclude(id=product.id)
    context = {
        'product': product,
        'comments': comments,
        'products': products,
    }
    return render(request, 'online_shop/detail.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from online_shop.models import Product, Comment


def comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        name = request.POST.get("name")
        comment_text = request.POST.get("comment")

        Comment.objects.create(
            name=name,
            comment=comment_text,
            owner=product,
        )

        return redirect("product_details", product_id=product_id)

    return redirect("product_details", product_id=product_id)


def filter(request, command):
    products = Product.objects.all().order_by(f'{command}')
    categories = Category.objects.all()
    for product in products:
        product.rating_range = range(product.rating)
    context = {
        "categories": categories,
        'products': products,
    }
    return render(request, 'online_shop/home.html', context)

def admin(request):
    form=ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'online_shop/admin-page.html',context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductModelForm

def edit_object(request, product_id):
    obj = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ProductModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductModelForm(instance=obj)

    return render(request, 'online_shop/admin-page.html', {'form': form})


def delete_product(request, product_id):
    obj = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        obj.delete()
        return redirect('home')

    return render(request, 'online_shop/confirm-delete.html', {'product': obj})

