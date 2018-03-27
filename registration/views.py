from django.views import generic
from django.shortcuts import redirect
from django.views.generic.edit import FormMixin
from django.utils import timezone
from django.contrib import messages

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

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            data = form.clean()
            s = Student(first_name=data['first_name'], last_name=data['last_name'], email=data['email'],
                        previous_occupation=data['occupation'], course_referral=data['course_referral'],
                        Application_reason=data['motivation'])
            s.save()
            if data['day1'] and data['day2']:
                c = Choice(choice_text="Both", has_laptop=data['laptop'], attend_course=data['previous_attend'],
                           email=s)
                c.save()
            elif data['day1'] and not data['day2']:
                c = Choice(choice_text="Tuesday", has_laptop=data['laptop'], attend_course=data['previous_attend'],
                           email=s)
                c.save()
            else:
                c = Choice(choice_text="Thursday", has_laptop=data['laptop'], attend_course=data['previous_attend'],
                           email=s)
                c.save()
            messages.add_message(request, messages.SUCCESS, success_message)
            return redirect('registration:index')

    else:
        # ignore this, need to add a redirect if the form is not valid which for now is handled by html code
        form = SignupForm()

    return redirect('registration:index')