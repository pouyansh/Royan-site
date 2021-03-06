from django import forms

from apps.royan_admin.models import RoyanTucagene


class ChangeSystemInfoForm(forms.ModelForm):
    class Meta:
        model = RoyanTucagene
        fields = ['summary', 'logo', 'logo2', 'about', 'phone_number', 'address', 'address_english',
                  'fax', 'email', 'instagram', 'telegram', 'twitter', 'linkedin', 'moto']


class BlockForm(forms.Form):
    username = forms.CharField(initial="user", required=False)
