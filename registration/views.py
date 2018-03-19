from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect
from django.views.generic.edit import FormMixin
from django.utils import timezone

from .models import Choice, Student
from .forms import SignupForm


class IndexView(FormMixin, generic.ListView):
    template_name = 'registration/index.html'
    context_object_name = 'latest_question_list'
    form_class = SignupForm

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Student.objects.filter(join_date__lte=timezone.now()).order_by('-join_date')[:5]


# class DetailView(generic.DetailView):
#     model = Users
#     template_name = 'registration/detail.html'
#
#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now())
#
#
class ResultsView(generic.DetailView):
    model = Student
    template_name = 'registration/results.html'


def register(request):
    # question = get_object_or_404(Student, pk=users_id)
    # try:
    #     selected_choice = Student.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    #     return render(request, 'registration/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a choice.",
    #     })
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('registration:results', args=(question.id,)))

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
            return redirect('registration:index')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = SignupForm()

    return redirect('registration:index')