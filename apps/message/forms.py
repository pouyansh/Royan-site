from django import forms

from apps.message.models import Message


class CreateMessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['title', 'text']
