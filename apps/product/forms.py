from django import forms

from apps.product.models import *


class CreateCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'description']

