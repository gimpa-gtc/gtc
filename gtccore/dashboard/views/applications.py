from django.shortcuts import render
from django.views import View

from dashboard.models import Application


class ApplicationsView(View):
    '''Applications view'''
    template = 'dashboard/pages/applications.html'

    def get(self, request):
        applications = Application.objects.all().order_by('-created_at')
        context ={
            'applications': applications,
        }
        return render(request, self.template, context)
    

class AdmissionsView(View):
    '''Admissions view'''
    template = 'dashboard/pages/admissions.html'

    def get(self, request):
        context ={}
        return render(request, self.template, context)