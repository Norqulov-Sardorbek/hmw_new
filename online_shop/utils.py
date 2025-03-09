from models import Product
def fitering(search_query):
    products = Product.objects.all()
    if search_query=='expensive':
        return products.order_by('-expensive')
    elif search_query=='cheap':
        return products.order_by('-cheap')
    elif search_query=='rating':
        return products.aggregate