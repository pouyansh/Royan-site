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
    file = forms.FileField(required=False)


class CheckDataForm(forms.Form):
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


class SetReceivingDateForm(forms.Form):
    receiving_date = forms.CharField(max_length=30)
