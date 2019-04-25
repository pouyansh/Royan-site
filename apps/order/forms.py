from django import forms


class OrderServiceFrom(forms.Form):

    def __init__(self):
        super().__init__()
        self.fields['chert'] = forms.CharField(required=False, max_length=10)

    def clean(self):
        print("here")
        return super(OrderServiceFrom, self).clean()
