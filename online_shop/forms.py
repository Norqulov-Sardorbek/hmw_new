from django import forms

from online_shop.models import Product


class ProductForm(forms.Form):
    pass

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'