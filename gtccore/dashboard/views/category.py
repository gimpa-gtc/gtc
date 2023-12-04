import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.db.models import Q

from dashboard.models import CourseCategory
class CategoryListView(View):
    template = 'dashboard/pages/category.html'

    def get(self, request):
        context ={}
        return render(request, self.template, context)
    
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