from django import forms

from apps.tutorial.models import Tutorial


class AddTutorialForm(forms.ModelForm):

    class Meta:
        model = Tutorial
        fields = ['name', 'description']


class TutorialListAdminForm(forms.Form):
    tutorial_id = forms.CharField(max_length=10)

