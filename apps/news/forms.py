from django import forms

from apps.news.models import News


class AddNewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = ['title', 'summary', 'description',
                  'english_title', 'english_summary', 'english_description',
                  'image']
