from django import forms

from apps.product.models import *


class CreateCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'description']


class CategoryListAdminForm(forms.Form):
    category_id = forms.CharField(max_length=10)


class CreateProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'count', 'image']


class SearchProductForm(forms.Form):
    product = forms.CharField(max_length=30)


class ProductListAdminForm(forms.Form):
    product = forms.CharField(max_length=30)
    product_id = forms.CharField(max_length=10)
