from django import forms


class SignupForm(forms.Form):

    YES_ATTENDED = True
    NO_ATTENDED = False

    ATTENDED_CHOICES = (
        (YES_ATTENDED, 'Yes'),
        (NO_ATTENDED, 'No'),
    )

    first_name = forms.CharField(max_length=60, label="First Name", widget=forms.TextInput(
        attrs={'id': 'fname', 'class': 'form-control', 'required': True}))
    last_name = forms.CharField(max_length=60, widget=forms.TextInput(
        attrs={'id': 'lname', 'class': 'form-control', 'required': True}))
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'id': 'email', 'class': 'form-control', 'required': True, 'type': 'email'}))
    password = forms.CharField(max_length=60, widget=forms.PasswordInput(
        attrs={'id': 'password', 'class': 'form-control', 'required': True}))
    laptop = forms.ChoiceField(label="Do you have a personal laptop that you can bring to our meetings?", required=False, choices=ATTENDED_CHOICES, widget=forms.RadioSelect(
        attrs={'id': 'laptop', 'name': 'laptop', 'class': ' pull-left', 'required': True}))
    previous_attend = forms.ChoiceField(label="Did you previously attended one of our courses?", required=False, choices=ATTENDED_CHOICES, widget=forms.RadioSelect(
        attrs={'id': 'attended', 'name': 'attended', 'class': ' pull-left', 'required': True}))
    day1 = forms.BooleanField(label="Tuesday", required=False, widget=forms.CheckboxInput(
        attrs={'id': 'day1', 'name': 'day1', 'class': 'mycheckboxes'}))
    day2 = forms.BooleanField(label="Thursday", required=False, widget=forms.CheckboxInput(
        attrs={'id': 'day2', 'name': 'day2', 'class': 'mycheckboxes'}))
    occupation = forms.CharField(label="Tell us about your previous / current occupation.", max_length=60,
                                 widget=forms.TextInput(
        attrs={'id': 'occupation', 'class': 'form-control', 'required': True, 'maxlength': '60', 'placeholder':
            'Astronaut'}))
    course_referral = forms.CharField(label="How did you find out about this course?", max_length=30,
                                      widget=forms.TextInput(attrs={'id': 'referral', 'class': 'form-control',
                                                                    'required': True, 'maxlength': '30',
                                                                    'placeholder': 'Facebook, a friend, from the University...'}))
    motivation = forms.CharField(label="Please write a few words (in English) describing your reason / motivation for attending this course.", max_length=800,
                                 widget=forms.Textarea(attrs={'id': 'motivation', 'class': 'form-control',
                                                              'required': True, 'rows': "10", 'cols': "40",
                                                              'maxlength': '800'}))

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        laptop = cleaned_data.get('laptop')
        previous_attend = cleaned_data.get('previous_attend')
        day1 = cleaned_data.get('day1')
        day2 = cleaned_data.get('day2')
        occupation = cleaned_data.get('occupation')
        course_referral = cleaned_data.get('course_referral')
        motivation = cleaned_data.get('motivation')

        if not first_name and not last_name and not email and not password and not day1 and not day2 and not laptop and not \
                previous_attend and not occupation and not course_referral and not motivation:
            raise forms.ValidationError('All the information bust be inputed ')

        data = {'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password,
                'laptop': laptop,
                'previous_attend': previous_attend,
                'day1': day1,
                'day2': day2,
                'occupation': occupation,
                'course_referral': course_referral,
                'motivation': motivation,
                }
        return data