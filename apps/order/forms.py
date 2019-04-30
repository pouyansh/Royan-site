from django import forms


class OrderServiceFrom(forms.Form):
    order_id = forms.IntegerField()
    CHOICES = [(1, 1),
               (2, 2)]
    type = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=CHOICES,
    )
    final = forms.IntegerField(required=False)
    file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        columns = kwargs.pop('columns')
        super(OrderServiceFrom, self).__init__(*args, **kwargs)
        self.fields['order_id'].required = False
        self.fields['order_id'].initial = -1
        self.fields['type'].required = False
        for col in columns:
            if col[1] == "text":
                self.fields[str(col[0])] = forms.CharField(max_length=col[3])
            if col[1] == "number":
                self.fields[str(col[0])] = forms.IntegerField()
            if col[1] == "choice":
                self.fields[str(col[0])] = forms.ChoiceField(choices=col[3])
            self.fields[str(col[0])].label = col[2]
            self.fields[str(col[0])].required = False

    def clean_type(self):
        if not self.cleaned_data['type']:
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
