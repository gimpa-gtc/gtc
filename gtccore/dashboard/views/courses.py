from django.shortcuts import render
from django.views import View

from dashboard.models import Course, CourseCategory

class CoursesView(View):
    template = 'dashboard/pages/courses.html'

    def get(self, request):
        courses = Course.objects.all().order_by('-id')
        context ={
            'courses': courses
        }
        return render(request, self.template, context)

class CourseCategoriesView(View):
    '''Course categories view'''
    template = 'dashboard/pages/course_categories.html'

    def get(self, request):
        categories = CourseCategory.objects.all().order_by('-id')
        context ={
            'categories': categories
        }
        return render(request, self.template, context)