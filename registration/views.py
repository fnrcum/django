from django.views import generic
from django.shortcuts import redirect
from django.views.generic.edit import FormMixin
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import login, authenticate
from hashlib import md5

from .models import Choice, Student
from .forms import SignupForm


class IndexView(FormMixin, generic.ListView):
    template_name = 'registration/index.html'
    context_object_name = 'latest_question_list'
    form_class = SignupForm

    def get_queryset(self):

        return Student.objects.filter(join_date__lte=timezone.now()).order_by('-join_date')[:5]


class RegistrationView(FormMixin, generic.ListView):
    template_name = 'registration/registration.html'
    context_object_name = 'latest_question_list'
    form_class = SignupForm

    def get_queryset(self):

        return Student.objects.filter(join_date__lte=timezone.now()).order_by('-join_date')[:5]


class ResultsView(generic.DetailView):
    model = Student
    template_name = 'registration/results.html'


def register(request):
    success_message = "You have been signed up for Softvision Software Testing 6.0 Workshop. If you are one of the " \
                      "selected participants, you will receive an email with further details. Thank you for registering!"
    fail_message = "We encountered an error when registering you"

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            data = form.clean()
            password = md5(data['password'].encode('utf-8') + data['email'].encode('utf-8')).hexdigest()
            s = Student(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=password,
                        previous_occupation=data['occupation'], course_referral=data['course_referral'],
                        Application_reason=data['motivation'])
            s.save()
            choice_text = "Both" if data['day1'] and data['day2'] else "Tuesday" if data['day1'] and not data['day2'] else "Thursday"
            c = Choice(choice_text=choice_text, has_laptop=data['laptop'], attend_course=data['previous_attend'],
                       email=s)
            c.save()
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect('registration:registration')

    else:
        messages.add_message(request, messages.MessageFailure, fail_message)
        print("Error else")
        return redirect('registration:registration')

    return redirect('registration:registration')