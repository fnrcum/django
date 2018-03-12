from django import forms

from .models import Student, Choice


class SignupForm(forms.Form):

    first_name = forms.CharField(max_length=60, required=True)
    last_name = forms.CharField(max_length=60, required=True)
    email = forms.EmailField(max_length=254, required=True)
    day1 = forms.BooleanField()
    day2 = forms.BooleanField()

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        first_name = cleaned_data.get('fname')
        last_name = cleaned_data.get('lname')
        email = cleaned_data.get('email')
        day1 = cleaned_data.get('day1')
        day2 = cleaned_data.get('day2')

        if not first_name and not last_name and not email and not day1 or day2:
            raise forms.ValidationError('All the information bust be inputed')