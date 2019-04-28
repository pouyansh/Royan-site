from django import forms


class OrderServiceFrom(forms.Form):
    order_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        columns = kwargs.pop('columns')
        super(OrderServiceFrom, self).__init__(*args, **kwargs)
        self.fields['order_id'].required = False
        self.fields['order_id'].initial = -1
        for col in columns:
            if col[1] == "text":
                self.fields[str(col[0])] = forms.CharField(max_length=col[3])
            if col[1] == "number":
                self.fields[str(col[0])] = forms.IntegerField()
            if col[1] == "choice":
                self.fields[str(col[0])] = forms.ChoiceField(choices=col[3])
            self.fields[str(col[0])].label = col[2]
            self.fields[str(col[0])].required = False

