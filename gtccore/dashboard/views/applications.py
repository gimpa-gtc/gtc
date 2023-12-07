import csv
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Q
from django.contrib import messages
from dashboard.models import Admission, Applicant, Application
from gtccore.library.constants import ApplicationStatus


class ApplicationsView(View):
    '''Applications view'''
    template = 'dashboard/pages/applications.html'

    def get(self, request):
        query = request.GET.get('query')
        applications = Application.objects.all().order_by('-created_at')
        if query:
            applications = applications.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query) |
                Q(course__title__icontains=query) |
                Q(application_status__icontains=query) |
                Q(payment_mode__icontains=query) |
                Q(payment_status__icontains=query)
            ).order_by('-created_at')

        context ={
            'applications': applications,
        }
        return render(request, self.template, context)
    

class AdmissionsView(View):
    '''Admissions view'''
    template = 'dashboard/pages/admissions.html'

    def get(self, request):
        query = request.GET.get('query')
        admissions = Admission.objects.all().order_by('-created_at')
        if query:
            admissions = admissions.filter(
                Q(application__application_id__icontains=query) |
                Q(application__name__icontains=query) |
                Q(application__email__icontains=query) |
                Q(application__phone__icontains=query) |
                Q(application__course__title__icontains=query)
            ).order_by('-created_at')
        context ={
            'admissions': admissions,
        }
        return render(request, self.template, context)


class GiveAdmissionView(View):
    '''Give admission to applicant'''
    template = 'dashboard/pages/give-admission.html'

    def get(self, request):
        pending_applications = Application.objects.filter(
            application_status=ApplicationStatus.PENDING.name
        ).count() # noqa
        approved_applications = Application.objects.filter(
            application_status=ApplicationStatus.APPROVED.name
        ).count() # noqa
        rejected_applications = Application.objects.filter(
            application_status=ApplicationStatus.REJECTED.name
        ).count() # noqa

        context = {
            'pending_applications': pending_applications,
            'approved_applications': approved_applications,
            'rejected_applications': rejected_applications,
        }
        return render(request, self.template, context)

    def post(self, request):
        admission_type = request.POST.get('admission_type')

        applications = None
        if admission_type == 'pending':
            print('admitting pending applications')
            applications = Application.objects.filter(
                application_status=ApplicationStatus.PENDING.name
            ).order_by('-created_at')

        elif admission_type == 'all':
            print('admitting rejected applications')
            applications = Application.objects.filter(
                Q(application_status=ApplicationStatus.REJECTED.name) | 
                Q(application_status=ApplicationStatus.PENDING.name) # noqa
            ).order_by('-created_at')

        else:
            messages.error(request, 'Invalid Admission Type')
            return redirect('dashboard:give_admission')
        num_applications = applications.count()
        if applications:
            for application in applications:
                application.application_status = ApplicationStatus.APPROVED.name
                application.save()
            
            messages.success(request, f'{num_applications} Applications Admitted Successfully') # noqa
            return redirect('dashboard:give_admission')
        else:
            messages.error(request, 'No Applications Found')
            return redirect('dashboard:give_admission')
        



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