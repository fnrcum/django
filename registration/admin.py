from django.contrib import admin

from .models import Student, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class StudentsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['first_name', 'last_name', 'email']}),
        # ('Date information', {'fields': ['join_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('first_name', 'last_name', 'email', 'join_date')
    list_filter = ['choice__choice_text']
    search_fields = ['first_name', 'last_name', 'email', 'join_date', 'choice__choice_text']

    def get_queryset(self, request):
        return self.model.objects.filter(choice__choice_text__in=["Tuesday", "Thursday"])


class StudentBoth(Student):
    class Meta:
        proxy = True


class StudentBothAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['first_name', 'last_name', 'email']}),
        # ('Date information', {'fields': ['join_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('first_name', 'last_name', 'email', 'join_date')
    # list_filter = ['choice__choice_text']
    search_fields = ['first_name', 'last_name', 'email', 'join_date', 'choice__choice_text']

    def get_queryset(self, request):
        return self.model.objects.filter(choice__choice_text="Both")


admin.site.register(Student, StudentsAdmin)
admin.site.register(StudentBoth, StudentBothAdmin)
admin.site.register(Choice)