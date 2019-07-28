from django import forms

from apps.research.models import ResearchArea, Paper


class AddResearchAreaForm(forms.ModelForm):

    class Meta:
        model = ResearchArea
        fields = ['name', 'description']


class ResearchAreaListAdminForm(forms.Form):
    research_area_id = forms.CharField(max_length=10)


class AddPaperForm(forms.ModelForm):

    class Meta:
        model = Paper
        fields = ['title', 'authors', 'summary', 'paper', 'link']


class PaperListAdminForm(forms.Form):
    paper_id = forms.CharField(max_length=10)

