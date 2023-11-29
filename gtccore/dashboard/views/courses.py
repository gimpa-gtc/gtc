from django.shortcuts import render
from django.views import View

from dashboard.models import Course

class InvoiceListView(View):
    template = 'dashboard/pages/courses.html'

    def get(self, request):
        courses = Course.objects.all().order_by('-id')
        context ={
            'courses': courses
        }
        return render(request, self.template, context)