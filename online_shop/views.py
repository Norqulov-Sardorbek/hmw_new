from django.shortcuts import render, get_object_or_404,redirect
from online_shop.models import Product, Comment, Category
from django.db.models import Q

# Create your views here.

def home(request):
    products = Product.objects.all()
    query = request.GET.get("query")
    categories = Category.objects.all()




    if query:
        products = products.filter(Q(name__icontains=query)|Q(description__icontains=query))

    for product in products:
        product.rating_range = range(product.rating)
    context = {
        'products': products,
        "categories": categories,

    }
    return render(request, 'online_shop/home.html',context=context)


def home_category(request , category):
    products = Product.objects.all().filter(category=category)
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'online_shop/home.html',context=context)



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

def filter(request, command ):
    products = Product.objects.all().order_by(f'{command}')
    for product in products:
        product.rating_range = range(product.rating)
    context = {
        'products': products,
    }
    return render(request, 'online_shop/home.html', context)