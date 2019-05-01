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


class CreateFormForm(forms.Form):
    final = forms.CharField(max_length=20)
    name = forms.CharField(max_length=30)
    type = forms.ChoiceField(choices=[("text", "text"), ("number", "number"), ("choice", "choice")])
    description = forms.CharField(max_length=100)
    file = forms.FileField()
    field_id = forms.IntegerField()

