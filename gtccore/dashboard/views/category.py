import csv
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Q
from django.contrib import messages
from dashboard.forms import CohortForm, CourseCategoryForm

from dashboard.models import Cohort, CourseCategory

class CourseCategoriesView(View):
    '''Course categories view'''
    template = 'dashboard/pages/course_categories.html'

    def get(self, request):
        query = request.GET.get('query')
        categories = CourseCategory.objects.all().order_by('-id')
        if query:
            categories = CourseCategory.objects.filter(
                Q(name__icontains=query)
            ).order_by('-id')
        context ={
            'categories': categories
        }
        return render(request, self.template, context)
    

class CreateUpdateCourseCategoryView(View):
    '''Create and update course category view'''
    template = 'dashboard/pages/create-update-course-category.html'

    def get(self, request):
        category_id = request.GET.get('category_id')
        category = None
        if category_id:
            category = CourseCategory.objects.filter(id=category_id).first()
        context = {
            'category': category
        }
        return render(request, self.template, context)
    
    def post(self, request):
        category_id = request.POST.get('category_id')
        category = None
        if category_id:
            category = CourseCategory.objects.filter(id=category_id).first()
        form = CourseCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            if category is None:
                messages.success(request, 'Category Created Successfully.')
                return redirect('dashboard:course_categories')
            messages.success(request, 'Category Updated Successfully.')
            return redirect('dashboard:course_categories')
        else:
            for k, v in form.errors.items():
                messages.error(request, f"{k}: {v}")
                return redirect('dashboard:course_categories')
    
class DownloadCategoriesView(View):
    '''Download categories as csv'''
    def get(self, request):
        categories = CourseCategory.objects.all().order_by('-id')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="categories.csv"'
        writer = csv.writer(response)
        writer.writerow(['name', 'created_at'])
        for category in categories:
            writer.writerow([category.name, category.created_at])
        return response
    

class CohortsView(View):
    template = 'dashboard/pages/cohorts.html'

    def get(self, request):
        cohorts = Cohort.objects.all().order_by('-id')
        query = request.GET.get('query')
        if query:
            cohorts = Cohort.objects.filter(
                Q(name__icontains=query) | 
                Q(start_month__icontains=query)
            ).order_by('-id')
        context ={
            'cohorts': cohorts
        }
        return render(request, self.template, context)
    

class CreateUpdateCohortView(View):
    template = 'dashboard/pages/create-update-cohort.html'

    def get(self, request):
        cohort_id = request.GET.get('cohort_id')
        cohort = None
        if cohort_id:
            cohort = Cohort.objects.filter(id=cohort_id).first()

        months = ['January','February','March','April','May','June','July','August','September','October','November','December']
        context ={
            'months': months,
            'cohort': cohort
        }
        return render(request, self.template, context)
    
    def post(self, request):
        cohort_id = request.POST.get('cohort_id')
        cohort = None
        if cohort_id:
            cohort = Cohort.objects.filter(id=cohort_id).first()
        form = CohortForm(request.POST, instance=cohort)
        if form.is_valid():
            form.save()
            if cohort is None:
                messages.success(request, 'Cohort created successfully.')
                return redirect('dashboard:cohorts')
            messages.success(request, 'Cohort Updated successfully.')
            return redirect('dashboard:cohorts')
        else:
            for k, v in form.errors.items():
                messages.error(request, f"{k}: {v}")
                return redirect('dashboard:cohorts')
    
class DownloadCohortView(View):
    '''Download cohorts as csv'''
    def get(self, request):
        cohorts = Cohort.objects.all().order_by('-id')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="cohorts.csv"'
        writer = csv.writer(response)
        writer.writerow(['name', 'start_month', 'created_at'])
        for cohort in cohorts:
            writer.writerow([cohort.name,cohort.start_month ,cohort.created_at])
        return response