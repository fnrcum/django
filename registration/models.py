from django.db import models
from django.utils import timezone

import datetime


class Student(models.Model):

    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=200)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} {1} email: {2}".format(self.first_name, self.last_name, self.email)

    # def join_date(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.pub_date <= now
    #
    # join_date.admin_order_field = 'pub_date'
    # join_date.boolean = True
    # join_date.short_description = 'Published recently?'


class Choice(models.Model):
    email = models.ForeignKey(Student, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text