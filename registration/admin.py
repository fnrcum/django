from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


from .models import Student, Choice


class DayChosenListFilter(admin.SimpleListFilter):
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


class HasLaptopListFilter(admin.SimpleListFilter):
    title = _('laptop availability')
    parameter_name = 'choice__has_laptop'

    def lookups(self, request, model_admin):
        return (
            ('Y', _('Yes ({})'.format(Student.objects.filter(choice__has_laptop=True).count()))),
            ('N', _('No ({})'.format(Student.objects.filter(choice__has_laptop=False).count()))),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Y':
            return queryset.filter(choice__has_laptop=True)
        if self.value() == 'N':
            return queryset.filter(choice__has_laptop=False)


class AddendedBeforeListFilter(admin.SimpleListFilter):
    title = _('previous attendance')
    parameter_name = 'choice__attend_course'

    def lookups(self, request, model_admin):
        return (
            ('Y', _('Yes ({})'.format(Student.objects.filter(choice__attend_course=True).count()))),
            ('N', _('No ({})'.format(Student.objects.filter(choice__attend_course=False).count()))),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Y':
            return queryset.filter(choice__attend_course=True)
        if self.value() == 'N':
            return queryset.filter(choice__attend_course=False)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class StudentsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['first_name', 'last_name', 'email', 'previous_occupation', 'course_referral', 'Application_reason']}),
        # ('Date information', {'fields': ['join_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('first_name', 'last_name', 'email', 'previous_occupation', 'course_referral', 'Application_reason', 'join_date')
    list_filter = (DayChosenListFilter, HasLaptopListFilter, AddendedBeforeListFilter,)
    search_fields = ['first_name', 'last_name', 'email', 'join_date', 'choice__choice_text']

    def get_queryset(self, request):
        return self.model.objects.filter(choice__choice_text__in=["Both", "Tuesday", "Thursday"])


class StudentBoth(Student):
    class Meta:
        proxy = True


class StudentBothAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['first_name', 'last_name', 'email', 'previous_occupation', 'course_referral', 'Application_reason']}),
        # ('Date information', {'fields': ['join_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('first_name', 'last_name', 'email', 'previous_occupation', 'course_referral', 'Application_reason', 'join_date')
    list_filter = (HasLaptopListFilter, AddendedBeforeListFilter,)
    search_fields = ['first_name', 'last_name', 'email', 'join_date', 'choice__choice_text']

    def get_queryset(self, request):
        return self.model.objects.filter(choice__choice_text="Both")


admin.site.register(Student, StudentsAdmin)
admin.site.register(StudentBoth, StudentBothAdmin)
admin.site.register(Choice)