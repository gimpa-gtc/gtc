from django import forms

from dashboard.models import Application, Comment, Course, CourseCategory, Faq


class ApplicationForm(forms.ModelForm):
    '''Application form.'''
    class Meta:
        model = Application
        fields = ['name', 'email', 'phone']