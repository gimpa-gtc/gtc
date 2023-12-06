from django import forms

from dashboard.models import Application, Comment, Course, CourseCategory, Faq, Facilitator


class ApplicationForm(forms.ModelForm):
    '''Application form.'''
    class Meta:
        model = Application
        fields = ['name', 'email', 'phone']


class FacilitatorForm(forms.ModelForm):
    '''Facilitator form.'''
    class Meta:
        model = Facilitator
        fields = ['name', 'title', 'image', 'specialization']