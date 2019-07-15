import re

from django import forms


class OligoSequenceField(forms.CharField):
    def clean(self, value):
        if value:
            if bool(re.match('^[A-Za-z]+$', value)):
                return value
            else:
                raise forms.ValidationError("این رشته تنها باید از حروف انگلیسی تشکیل شود")
        return value


class OrderServiceFrom(forms.Form):
    final = forms.IntegerField(required=False)
    order_id = forms.IntegerField()
    CHOICES = [(1, 1),
               (2, 2)]
    type = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=CHOICES,
    )
    file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        columns = kwargs.pop('columns')
        super(OrderServiceFrom, self).__init__(*args, **kwargs)
        self.fields['order_id'].required = False
        self.fields['order_id'].initial = -1
        self.fields['final'].initial = -1
        self.fields['type'].required = False
        for col in columns:
            if col[1] == "text":
                self.fields[str(col[0])] = forms.CharField(max_length=col[3])
            if col[1] == "number":
                self.fields[str(col[0])] = forms.IntegerField()
            if col[1] == "choice":
                self.fields[str(col[0])] = forms.ChoiceField(choices=col[3])
            if col[1] == "oligo":
                self.fields[str(col[0])] = OligoSequenceField(max_length=col[3])
            self.fields[str(col[0])].label = col[2]
            self.fields[str(col[0])].required = False

    def clean_type(self):
        if not self.cleaned_data['type'] and str(self.cleaned_data['final']) != "-1":
            raise forms.ValidationError("باید حداقل یکی از این دو مورد را انتخاب کنید")
        return self.cleaned_data['type']

    def clean(self):
        return super(OrderServiceFrom, self).clean()


class CheckDataFrom(forms.Form):
    confirm = forms.BooleanField(required=True)
    name = forms.CharField(max_length=40)

    def clean_confirm(self):
        confirm = self.cleaned_data['confirm']
        if not confirm:
            raise forms.ValidationError("باید صحبت اطلاعات را تایید کنید.")


class SetInvoiceForm(forms.Form):
    payment = forms.IntegerField()

    def clean_payment(self):
        payment = self.cleaned_data['payment']
        if payment < 0:
            raise ValueError("هزینه نمی‌تواند منفی باشد.")
        return payment
