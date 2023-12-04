import csv
from django.http import HttpResponse
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
    
class DownloadApplicationsView(View):
    '''Download applications as csv'''
    def get(self, request):
        applications = Application.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="applications.csv"'
        writer = csv.writer(response)
        writer.writerow(['application_id', 'name', 'email', 'phone', 'course', 'application_status', 'payment_mode', 'payment_status','created_at']) # noqa
        for application in applications:
            writer.writerow([application.application_id, application.name, application.email, application.phone, application.course, application.application_status, application.payment_mode, application.payment_status, application.created_at]) # noqa
        return response
    
class DownloadApplicantsView(View):
    '''Download applicants as csv'''
    def get(self, request):
        applicants = Applicant.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="applicants.csv"'
        writer = csv.writer(response)
        writer.writerow(['name', 'email', 'phone', 'created_at'])
        for applicant in applicants:
            writer.writerow([applicant.name, applicant.email, applicant.phone, applicant.created_at]) # noqa
        return response
    
class DownloadAdmissionsView(View):
    '''Download admissions as csv'''
    def get(self, request):
        admissions = Admission.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="admissions.csv"'
        writer = csv.writer(response)
        writer.writerow(['application_id', 'name', 'email', 'phone', 'course', 'created_at']) # noqa
        for admission in admissions:
            writer.writerow([admission.application.application_id, admission.application.name, admission.application.email, admission.application.phone, admission.application.course, admission.created_at]) # noqa
        return response