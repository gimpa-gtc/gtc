from django import forms

from dashboard.models import (Application, Cohort, Comment, Contact, Course,
                              CourseCategory, CustomCourseRequest, Facilitator, Notification)


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


class CohortForm(forms.ModelForm):
    '''Cohort form.'''
    class Meta:
        model = Cohort
        fields = ['name', 'start_month']


class CourseForm(forms.ModelForm):
    '''Course form.'''
    class Meta:
        model = Course
        exclude = ['cohort', 'category']


class CourseCategoryForm(forms.ModelForm):
    '''Course category form.'''
    class Meta:
        model = CourseCategory
        fields = ['name']

class NotificationForm(forms.ModelForm):
    '''Notification form.'''
    class Meta:
        model = Notification
        fields = ['title', 'content']

class ContactUsForm(forms.ModelForm):
    '''Contact us form.'''
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']

class CustomCourseReguestForm(forms.ModelForm):
    '''Contact us form.'''
    class Meta:
        model = CustomCourseRequest
        fields = ['name', 'email', 'phone', 'message']