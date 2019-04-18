from django import forms


class OrderServiceFrom(forms.Form):
    extra_field_count = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__()
        columns = kwargs.pop('columns')
        extra_fields = kwargs.pop('extra', 1)
        self.fields['extra_field_count'].initial = extra_fields

        for index in range(int(extra_fields)):
            for col in columns:
                if col[1] == "text":
                    self.fields[str(col[0])+'_{index}'.format(index=index)] = forms.CharField(max_length=col[3])
                if col[1] == "number":
                    self.fields[str(col[0])+'_{index}'.format(index=index)] = forms.IntegerField()
                if col[1] == "choice":
                    self.fields[str(col[0])+'_{index}'.format(index=index)] = forms.ChoiceField(choices=col[3])
                self.fields[str(col[0])+'_{index}'.format(index=index)].label = col[2]

