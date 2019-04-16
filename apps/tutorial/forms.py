from django import forms

from apps.research.models import ResearchArea


class AddResearchAreaForm(forms.ModelForm):

    class Meta:
        model = ResearchArea
        fields = ['name', 'description']


class ResearchAreaListAdminForm(forms.Form):
    research_area_id = forms.CharField(max_length=10)

