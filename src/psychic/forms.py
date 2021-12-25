from django import forms
from django.core.exceptions import ValidationError


class RenewForm(forms.Form):
    number = forms.IntegerField()

    def clean_number(self):
        data = self.cleaned_data['number']
        if not (isinstance(data, int) and 10 <= data <= 99):
            raise ValidationError('Введено не двухзначное число')
        return data
