import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from dashboard.models import Cohort, Course, CourseCategory

class CoursesView(View):
    template = 'dashboard/pages/courses.html'

    def get(self, request):
        courses = Course.objects.all().order_by('-id')
        context ={
            'courses': courses
        }
        return render(request, self.template, context)
    
class CreateUpdateCourseView(View):
    template = 'dashboard/pages/create_update_course.html'

    def get(self, request):
        categories = CourseCategory.objects.all()
        cohorts = Cohort.objects.all()
        context ={
            'categories': categories,
            'cohorts': cohorts
        }
        return render(request, self.template, context)


    
class DownloadCoursesView(View):
    '''Download courses as csv'''
    def get(self, request):
        courses = Course.objects.all().order_by('-id')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="courses.csv"'
        writer = csv.writer(response)
        writer.writerow(['title', 'description', 'details', 'category', 'start_date', 'end_date', 'price', 'duration', 'class_days', 'class_time', 'teachers', 'student_capacity', 'requirements', 'syllabus', 'thumbnail', 'created_at']) # noqa
        for course in courses:
            writer.writerow([course.title, course.description, course.details, course.category, course.start_date, course.end_date, course.price, course.duration, course.class_days, course.class_time, course.teachers, course.student_capacity, course.requirements, course.syllabus, course.thumbnail, course.created_at]) # noqa
        return response