from django.shortcuts import render
from django.views import View
from django.db.models import Q
from dashboard.models import Admission, Applicant, Application


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
        admissions = Admission.objects.all().order_by('-created_at')
        context ={
            'admissions': admissions,
        }
        return render(request, self.template, context)
    

class ApplicantsView(View):
    '''applicants view'''
    template = 'dashboard/pages/applicants.html'

    def get(self, request):
        applicants = Applicant.objects.all().order_by('-created_at')
        context ={
            'applicants': applicants,
        }
        return render(request, self.template, context)