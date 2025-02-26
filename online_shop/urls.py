from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('product/<int:product_id>/', views.details, name='product_details'),
    path('comment/<int:product_id>/', views.comment, name='comment'),
    path('home_category/<str:category>/', views.home_category, name='home_category'),
    path('filter/<str:command>/',views.filter, name='filter'),
]
