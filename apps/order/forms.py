from django import forms


class OrderServiceFrom(forms.Form):

    def __init__(self, *args, **kwargs):
        columns = kwargs.pop('columns')
        super(OrderServiceFrom, self).__init__(*args, **kwargs)
        for col in columns:
            if col[1] == "text":
                self.fields[str(col[0])] = forms.CharField(max_length=col[3])
            if col[1] == "number":
                self.fields[str(col[0])] = forms.IntegerField()
            if col[1] == "choice":
                self.fields[str(col[0])] = forms.ChoiceField(choices=col[3])
            self.fields[str(col[0])].label = col[2]

    def clean(self):
        print("here")
        return super(OrderServiceFrom, self).clean()
