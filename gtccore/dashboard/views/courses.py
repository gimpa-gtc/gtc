import csv
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib import messages
from django.views import View
from dashboard.forms import CourseForm

from dashboard.models import Cohort, Course, CourseCategory

class CoursesView(View):
    template = 'dashboard/pages/courses.html'

    def get(self, request):
        query = request.GET.get('query')
        courses = Course.objects.all().order_by('-id')
        if query:
            courses = Course.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(details__icontains=query) | 
                Q(category__name__icontains=query) | 
                Q(start_date__icontains=query) | 
                Q(end_date__icontains=query) | 
                Q(price__icontains=query) | 
                Q(duration__icontains=query) | 
                Q(class_days__icontains=query) | 
                Q(class_time__icontains=query) | 
                Q(location__icontains=query) | 
                Q(student_capacity__icontains=query) | 
                Q(requirements__icontains=query) | 
                Q(syllabus__icontains=query)
            ).order_by('-id')
        context ={
            'courses': courses
        }
        return render(request, self.template, context)
    
class CreateUpdateCourseView(View):
    template = 'dashboard/pages/create-update-course.html'

    def get(self, request):
        course_id = request.GET.get('course_id')
        course = None
        if course_id:
            course = Course.objects.filter(id=course_id).first()
        categories = CourseCategory.objects.all()
        cohorts = Cohort.objects.all()
        context ={
            'categories': categories,
            'cohorts': cohorts,
            'course': course
        }
        return render(request, self.template, context)
    
    def post(self, request):
        course_id = request.POST.get('course_id')
        cohort_id = request.POST.get('cohort_id')
        category_id = request.POST.get('category_id')
        category = CourseCategory.objects.filter(id=category_id).first()
        cohort = Cohort.objects.filter(id=cohort_id).first()
        if not category:
            messages.error(request, 'Category Not Found')
            return redirect('dashboard:courses')
        
        course = None
        if course_id:
            course = Course.objects.filter(id=course_id).first()
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            item = form.save(commit=False)
            item.category = category
            item.cohort = cohort
            item.save()
            if course is not None:
                messages.success(request, 'Course Updated successfully')
                return redirect('dashboard:courses')
            messages.success(request, 'Course Saved successfully')
            return redirect('dashboard:courses')
        else:
            for k, v in form.errors.items():
                messages.error(request, f"{k}: {v}")
                return redirect('dashboard:courses')


    
class DownloadCoursesView(View):
    '''Download courses as csv'''
    def get(self, request):
        courses = Course.objects.all().order_by('-id')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="courses.csv"'
        writer = csv.writer(response)
        writer.writerow(['title', 'description', 'details', 'category','cohort', 'start_date', 'end_date', 'price', 'duration', 'class_days', 'class_time', 'location', 'student_capacity', 'requirements', 'syllabus', 'thumbnail', 'created_at']) # noqa
        for course in courses:
            cohort = course.cohort.name if course.cohort else ''
            writer.writerow([course.title, course.description, course.details, course.category, cohort ,course.start_date, course.end_date, course.price, course.duration, course.class_days, course.class_time, course.location, course.student_capacity, course.requirements, course.syllabus, course.thumbnail, course.created_at]) # noqa
        return response