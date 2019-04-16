from django import forms

from apps.research.models import ResearchArea


class AddResearchAreaForm(forms.ModelForm):

    class Meta:
        model = ResearchArea
        fields = ['name', 'description']
