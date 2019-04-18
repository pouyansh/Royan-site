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
        columns = kwargs.pop('columns')
        for col in columns:
            if col[1] == "text":
                self.fields[col[0]] = forms.CharField(max_length=col[3])
            if col[1] == "number":
                self.fields[col[0]] = forms.IntegerField()
            if col[1] == "choice":
                self.fields[col[0]] = forms.ChoiceField(choices=col[3])
            self.fields[col[0]].label = col[2]

