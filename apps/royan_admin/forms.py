from django import forms

from apps.royan_admin.models import RoyanTucagene


class ChangeSystemInfoForm(forms.ModelForm):

    class Meta:
        model = RoyanTucagene
        fields = ['summary', 'logo', 'about', 'phone_number', 'address', 'fax', 'email']


class BlockForm(forms.Form):
    username = forms.CharField(initial="user", required=False)
