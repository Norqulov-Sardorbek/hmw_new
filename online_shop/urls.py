from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.details, name='product_details'),
    path('comment/<int:product_id>/', views.comment, name='comment'),
    path('home_category/<str:category>/', views.home, name='home_category'),
    path('filter/<str:command>/', views.filter, name='filter'),
    path('admin-page/', views.admin, name='admin-page'),
    path('edit-product/<int:product_id>/', views.edit_object, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('order-view/<int:pk>/', views.order_view, name='order_view')
]
