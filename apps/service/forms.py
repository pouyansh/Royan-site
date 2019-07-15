from django import forms

from apps.service.models import *


class CreateFieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['name', 'description', 'image']


class FieldListAdminForm(forms.Form):
    field_id = forms.CharField(max_length=10)


class CreateServiceForm(forms.ModelForm):
    field = forms.CharField(max_length=10)

    class Meta:
        model = Service
        fields = ['name', 'description', 'photo']


class UpdateServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'photo']


class ServiceListAdminForm(forms.Form):
    service_id = forms.CharField(max_length=10)


class CreateFormForm(forms.Form):
    final = forms.CharField(max_length=20, required=False)
    name = forms.CharField(max_length=30, required=False)
    type = forms.ChoiceField(
        choices=[("text", "text"), ("number", "number"), ("choice", "choice"), ("oligo", "oligo")])
    description = forms.CharField(max_length=100, required=False)
    file = forms.FileField(required=False)
    field_id = forms.IntegerField(required=False)
