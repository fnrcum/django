from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


from .models import Student, Choice


class DecadeBornListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('the day chosen')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'choice__choice_text'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('Both', _('Both ({})'.format(Student.objects.filter(choice__choice_text="Both").count()))),
            ('Tuesday', _('Tuesday ({})'.format(Student.objects.filter(choice__choice_text="Tuesday").count()))),
            ('Thursday', _('Thursday ({})'.format(Student.objects.filter(choice__choice_text="Thursday").count()))),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'Both':
            return queryset.filter(choice__choice_text="Both")
        if self.value() == 'Tuesday':
            return queryset.filter(choice__choice_text="Tuesday")
        if self.value() == 'Thursday':
            return queryset.filter(choice__choice_text="Thursday")


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class StudentsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['first_name', 'last_name', 'email']}),
        # ('Date information', {'fields': ['join_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('first_name', 'last_name', 'email', 'join_date')
    list_filter = (DecadeBornListFilter,)
    search_fields = ['first_name', 'last_name', 'email', 'join_date', 'choice__choice_text']

    def get_queryset(self, request):
        return self.model.objects.filter(choice__choice_text__in=["Both", "Tuesday", "Thursday"])


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
    # list_filter = (DecadeBornListFilter,)
    search_fields = ['first_name', 'last_name', 'email', 'join_date', 'choice__choice_text']

    def get_queryset(self, request):
        return self.model.objects.filter(choice__choice_text="Both")


admin.site.register(Student, StudentsAdmin)
admin.site.register(StudentBoth, StudentBothAdmin)
admin.site.register(Choice)