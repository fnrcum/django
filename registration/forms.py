from django import forms


class SignupForm(forms.Form):

    first_name = forms.CharField(max_length=60, label="First Name", widget=forms.TextInput(
        attrs={'id': 'fname', 'class': 'form-control', 'required': True}))
    last_name = forms.CharField(max_length=60, widget=forms.TextInput(
        attrs={'id': 'lname', 'class': 'form-control', 'required': True}))
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'id': 'email', 'class': 'form-control', 'required': True, 'type': 'email'}))
    day1 = forms.BooleanField(label="Tuesday", initial=True, required=False, widget=forms.CheckboxInput(
        attrs={'id': 'day1', 'name': 'day1', 'checked': ''}))
    day2 = forms.BooleanField(label="Thursday", required=False, widget=forms.CheckboxInput(
        attrs={'id': 'day2', 'name': 'day2'}))

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        day1 = cleaned_data.get('day1')
        day2 = cleaned_data.get('day2')

        if not first_name and not last_name and not email and not day1 and not day2:
            raise forms.ValidationError('All the information bust be inputed')

        data = {'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'day1': day1,
                'day2': day2}
        return data