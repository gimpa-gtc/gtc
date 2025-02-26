import csv

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.forms import ApplicationForm
from dashboard.models import (Admission, Applicant, Application, Course,
                              CourseCategory)
from gtccore.library.constants import ApplicationStatus
from gtccore.library.decorators import StaffLoginRequired
from gtccore.library.logs import log_user_activity


class ApplicationsView(PermissionRequiredMixin, View):
    '''Applications view'''
    template = 'dashboard/pages/applications.html'
    permission_required = ['dashboard.view_application']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        query = request.GET.get('query')
        filtered = request.GET.get('form_id') == 'filter'
        applications = Application.objects.all().order_by('-created_at')
        course_categories = CourseCategory.objects.all().order_by('name')
        if query:
            query = query.strip()
            applications = applications.filter(
                Q(application_id__icontains=query) |
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query) |
                Q(course__title__icontains=query) |
                Q(application_status__icontains=query) |
                Q(payment_mode__icontains=query) |
                Q(payment_status__icontains=query)
            ).order_by('-created_at')
        
        if filtered:
            category = request.GET.get('category')
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if category == 'all':
                pass # All applications are already filtered
            else:
                applications = applications.filter(course__category__id=category)
            if start_date:
                applications = applications.filter(course__start_date__gte=start_date)
            if end_date:
                applications = applications.filter(course__start_date__lte=end_date)

        context = {
            'applications': applications,
            'categories': course_categories,
            'selected_category': request.GET.get('category') or 'all',
            'start_date': request.GET.get('start_date') or '',
            'end_date': request.GET.get('end_date') or '',
        }
        return render(request, self.template, context)


class CreateApplicationView(PermissionRequiredMixin, View):
    '''Create application view'''
    template = 'dashboard/pages/create-application.html'
    permission_required = [
        'dashboard.add_application',
        'dashboard.change_application',
    ]

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        courses = Course.objects.all().order_by('title')
        context = {
            'courses': courses,
        }
        return render(request, self.template, context)
    

    @method_decorator(StaffLoginRequired)
    def post(self, request):
        course_id = request.POST.get('course_id')
        course = Course.objects.filter(id=course_id).first()

        if not course:
            messages.error(request, 'Invalid Course')
            return redirect('dashboard:create_update_application')
        
        form = ApplicationForm(request.POST, request.FILES)
        if not form.is_valid():
            for k, v in form.errors.items():
                messages.error(request, f"{k}: {v}")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        new_application = form.save(commit=False)
        new_application.course = course                
        new_application.save()
        log_user_activity(request.user, 'Created application', None, new_application) # noqa
        messages.success(request, 'Application Created Successfully')
        return redirect('dashboard:applications')
    

class AdmissionsView(PermissionRequiredMixin, View):
    '''Admissions view'''
    template = 'dashboard/pages/admissions.html'
    permission_required = ['dashboard.view_admission']

    @method_decorator(StaffLoginRequired)
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


class GiveAdmissionView(PermissionRequiredMixin, View):
    '''Give admission to applicant'''
    template = 'dashboard/pages/give-admission.html'
    permission_required = [
        'dashboard.add_admission',
    ]

    @method_decorator(StaffLoginRequired)
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

    @method_decorator(StaffLoginRequired)
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
        

class AdmitOneStudentView(PermissionRequiredMixin, View):
    '''Admit just one student'''
    template = 'dashboard/pages/admit_one_student.html' 
    permission_required = [
        'dashboard.add_admission',
    ]

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        application_id = request.GET.get('application_id')
        application = Application.objects.filter(application_id=application_id).first() # noqa
        context = {
            'application': application
        }
        return render(request, self.template, context)
    
    @method_decorator(StaffLoginRequired)
    def post(self, request):
        application_id = request.POST.get('application_id')
        application = Application.objects.filter(application_id=application_id).first() # noqa
        if application:
            application.application_status = ApplicationStatus.APPROVED.name
            application.save()
            # log user activity
            log_user_activity(request.user, 'Admitted student', application, None) # noqa
            messages.success(request, 'Student Admitted Successfully')
        else:
            messages.error(request, 'Application Not Found')
        return redirect('dashboard:applications')


class ApplicantsView(PermissionRequiredMixin, View):
    '''applicants view'''
    template = 'dashboard/pages/applicants.html'
    permission_required = ['dashboard.view_applicant']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        query = request.GET.get('query')
        applicants = Applicant.objects.all().order_by('-created_at')
        if query:
            query = query.strip()
            applicants = applicants.filter(
                Q(name__icontains=query) |
                Q(email__icontains=query) |
                Q(phone__icontains=query)
            ).order_by('-created_at')
        context ={
            'applicants': applicants,
        }
        return render(request, self.template, context)
    
class DownloadApplicationsView(PermissionRequiredMixin, View):
    '''Download applications as csv'''
    permission_required = ['dashboard.view_application']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        filtered_download = request.GET.get('form_id') == 'filter'
        category = request.GET.get('category')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        applications = Application.objects.all().order_by('-created_at')
        if filtered_download:
            if category == 'all':
                pass # All applications are already filtered
            else:
                applications = applications.filter(course__category__id=category)
            if start_date:
                applications = applications.filter(course__start_date__gte=start_date)
            if end_date:
                applications = applications.filter(course__start_date__lte=end_date)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="applications.csv"'
        writer = csv.writer(response)
        writer.writerow(['application_id', 'name', 'email', 'phone', 'dob', 'address_box_number', 'course', 'category', 'application_status', 'payment_mode', 'payment_status','created_at']) # noqa
        for application in applications:
            writer.writerow([application.application_id, application.name, application.email, application.phone, application.dob, application.box_address, application.course, application.course.category.name, application.application_status, application.payment_mode, application.get_payment_status(), application.created_at]) # noqa
        return response
    
class DownloadApplicantsView(PermissionRequiredMixin, View):
    '''Download applicants as csv'''
    permission_required = ['dashboard.view_applicant']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        applicants = Applicant.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="applicants.csv"'
        writer = csv.writer(response)
        writer.writerow(['name', 'email', 'phone', 'dob', 'address_box_number', 'created_at'])
        for applicant in applicants:
            writer.writerow([applicant.name, applicant.email, applicant.phone, applicant.dob, applicant.box_address, applicant.created_at]) # noqa
        return response
    
class DownloadAdmissionsView(PermissionRequiredMixin, View):
    '''Download admissions as csv'''
    permission_required = ['dashboard.view_admission']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        admissions = Admission.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="admissions.csv"'
        writer = csv.writer(response)
        writer.writerow(['application_id', 'name', 'email', 'phone', 'course', 'created_at']) # noqa
        for admission in admissions:
            writer.writerow([admission.application.application_id, admission.application.name, admission.application.email, admission.application.phone, admission.application.course, admission.created_at]) # noqa
        return response
    

class DeleteApplicationView(PermissionRequiredMixin, View):
    '''Delete application'''
    permission_required = ['dashboard.delete_application']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        application_id = request.GET.get('application_id')
        application = Application.objects.filter(application_id=application_id).first() # noqa
        if application:
            application.delete()
            messages.success(request, 'Application Deleted Successfully')
        else:
            messages.error(request, 'Application Not Found')
        return redirect('dashboard:applications')
    

class DeleteApplicantView(PermissionRequiredMixin, View):
    '''Delete applicant'''
    permission_required = ['dashboard.delete_applicant']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        applicant_id = request.GET.get('applicant_id')
        applicant = Applicant.objects.filter(id=applicant_id).first() # noqa
        if applicant:
            applicant.delete()
            messages.success(request, 'Applicant Deleted Successfully')
        else:
            messages.error(request, 'Applicant Not Found')
        return redirect('dashboard:applicants')