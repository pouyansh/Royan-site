from django import forms


class OrderServiceFrom(forms.Form):
    name = forms.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        super().__init__()
        columns = kwargs.pop('columns')
        for col in columns:
            if col[1] == "text":
                self.fields[col[0]] = forms.CharField(max_length=col[3])
            if col[1] == "number":
                self.fields[col[0]] = forms.IntegerField()
            if col[1] == "choice":
                self.fields[col[0]] = forms.ChoiceField(choices=col[3])
            self.fields[col[0]].label = col[2]

