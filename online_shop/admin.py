from django.contrib import admin

from online_shop.models import Product, Comment

# Register your models here.

admin.site.register(Product)
admin.site.register(Comment)