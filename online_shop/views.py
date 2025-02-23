from django.shortcuts import render, get_object_or_404
from online_shop.models import Product, Comment


# Create your views here.

def home(request):
    products = Product.objects.all()
    query = request.GET.get("query")




    if query:
        products = products.filter(name__icontains=query)


    for product in products:
        product.rating_range = range(product.rating)
    context = {
        'products': products,

    }
    return render(request, 'online_shop/home.html',context=context)





def details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(owner=product).order_by('-commented_date')
    recently_viewed = request.session.get("recently_viewed", [])

    if request.method == "POST":
        name = request.POST.get("name")
        comment_text = request.POST.get("comment")

        Comment.objects.create(
        name=name,
        comment=comment_text,
        owner=product,
    )

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
