from django import forms

from apps.service.models import *


class CreateFieldForm(forms.ModelForm):

    class Meta:
        model = Field
        fields = ['name', 'description']


class FieldListAdminForm(forms.Form):
    field_id = forms.CharField(max_length=10)


class CreateServiceForm(forms.ModelForm):
    field = forms.CharField(max_length=10)

    class Meta:
        model = Service
        fields = ['name', 'description']


class UpdateServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        fields = ['name', 'description']


class ServiceListAdminForm(forms.Form):
    service_id = forms.CharField(max_length=10)


class OrderServiceFrom(forms.Form):
    name = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        super().__init__()
        temp = kwargs.pop('temp')
        print(temp[0], temp[1])

