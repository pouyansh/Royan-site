from django import forms

from apps.tutorial.models import *


class AddTutorialForm(forms.ModelForm):

    class Meta:
        model = Tutorial
        fields = ['name', 'description']


class TutorialListAdminForm(forms.Form):
    tutorial_id = forms.CharField(max_length=10)


class WorkshopListAdminForm(forms.Form):
    workshop_id = forms.CharField(max_length=10)


class AddLinkForm(forms.ModelForm):

    class Meta:
        model = Links
        fields = ['title', 'description', 'link', 'rank', 'image']

