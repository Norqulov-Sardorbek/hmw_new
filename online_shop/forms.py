from django import forms

from online_shop.models import Product
from online_shop.models import Order
from phonenumber_field.formfields import PhoneNumberField

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ()





class OrderModelForm(forms.ModelForm):
    phone = PhoneNumberField(region='UZ')

    class Meta:
        model = Order
        exclude = ('product',)