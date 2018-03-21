from django.db import models


class Student(models.Model):

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=200)
    previous_occupation = models.TextField(default="Nothing")
    course_referral = models.CharField(max_length=200, default="Nothing")
    Application_reason = models.TextField(default="Nothing")
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} {1} email: {2}".format(self.first_name, self.last_name, self.email)


class Choice(models.Model):
    email = models.ForeignKey(Student, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    has_laptop = models.BooleanField(default=False)
    attend_course = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text