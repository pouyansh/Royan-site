from django import forms

from apps.service.models import *


class CreateFieldForm(forms.ModelForm):

    class Meta:
        model = Field
        fields = ['name', 'description']


class CreateServiceForm(forms.ModelForm):
    field = forms.CharField(max_length=10)

    class Meta:
        model = Service
        fields = ['name', 'description']
