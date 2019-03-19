from django import forms

from apps.product.models import *


class CreateCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'description']


class CategoryListAdminForm(forms.Form):
    category_id = forms.CharField(max_length=10)
