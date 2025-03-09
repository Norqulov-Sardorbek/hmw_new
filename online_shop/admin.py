from django.contrib.auth.models import Group

from django.contrib import admin
from django.utils.timezone import now
from online_shop.models import Product, Comment, Category

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from adminsortable2.admin import SortableAdminMixin


# Register your models here.


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ProductAdmin(SortableAdminMixin,
                   ImportExportModelAdmin, admin.ModelAdmin):
    resource_classes = [ProductResource]
    list_display = ['name', 'price', 'quantity', 'formatted_created_at', 'order']
    search_fields = ('name',)
    list_filter = ('category', 'created_at')
    ordering = ('order',)  # Ensure sorting works!

    class Media:
        js = ('https://cdnjs.cloudflare.com/ajax/libs/Sortable/2.0.0/Sortable.min.js', 'js/admin-sortable.js')


    def formatted_created_at(self, obj):
        if obj.created_at.year == now().year:
            return obj.created_at.strftime("%b %d")
        return obj.created_at.strftime("%b %d, %Y")

    formatted_created_at.admin_order_field = 'created_at'
    formatted_created_at.short_description = 'Created At'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'comment', 'formatted_commented_date')
    search_fields = ('name', 'owner__name')

    def formatted_commented_date(self, obj):
        if obj.commented_date.year == now().year:
            return obj.commented_date.strftime("%b %d")
        return obj.commented_date.strftime("%b %d, %Y")

    formatted_commented_date.admin_order_field = 'commented_date'
    formatted_commented_date.short_description = 'Commented At'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'formatted_created_at')

    def formatted_created_at(self, obj):
        if obj.created_at.year == now().year:
            return obj.created_at.strftime("%b %d")
        return obj.created_at.strftime("%b %d, %Y")

    formatted_created_at.admin_order_field = 'created_at'
    formatted_created_at.short_description = 'Created At'

admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.unregister(Group)
admin.site.site_header = "E-Commerce Admin"
admin.site.site_title = "E-Commerce Admin Portal"
admin.site.index_title = "Welcome to E-Commerce Shop"
