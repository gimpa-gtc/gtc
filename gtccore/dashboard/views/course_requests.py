import csv

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.models import CustomCourseRequest
from gtccore.library.decorators import StaffLoginRequired


class CourseRequestsView(PermissionRequiredMixin, View):
    '''Contact messages view'''
    template = 'dashboard/pages/course_requests.html'
    permission_required = ['dashboard.view_customcourserequest']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        query = request.GET.get('query')
        course_requests = CustomCourseRequest.objects.all().order_by('-id')
        if query:
            course_requests = CustomCourseRequest.objects.filter(
                Q(name__icontains=query)
            ).order_by('-id')
        context ={
            'course_requests': course_requests
        }
        return render(request, self.template, context)

class ReplyCourseRequestView(PermissionRequiredMixin, View):
    '''Reply message view'''
    template = 'dashboard/pages/reply_course_request.html'
    permission_required = ['dashboard.view_customcourserequest']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        request_id = request.GET.get('request_id')
        course_request = CustomCourseRequest.objects.filter(id=request_id).first()
        context = {
            'course_request': course_request
        }
        return render(request, self.template, context)
    
    @method_decorator(StaffLoginRequired)
    def post(self, request):
        request_id = request.POST.get('request_id')
        custom_request = CustomCourseRequest.objects.filter(id=request_id).first()
        title = request.POST.get('reply_title')
        message = request.POST.get('reply_message')
        if not custom_request:
            messages.error(request, 'Invalid Request.')
            return redirect('dashboard:course_requests')
        success = custom_request.reply_message(f"{title}\n\n{message}", mtype='sms')
        
        # update custom course request
        if success:
            custom_request.is_replied = True
            custom_request.replied_message = f"{title}\n\n{message}"
            custom_request.replied_by = request.user
            custom_request.replied_at = timezone.now()
            custom_request.save()
            messages.success(request, 'Message Replied Successfully.')
        else:
            messages.error(request, 'Failed to reply message.')
        return redirect('dashboard:course_requests')
    
class DownloadCourseRequestsView(PermissionRequiredMixin, View):
    '''Download contact messages view'''
    permission_required = ['dashboard.view_customcourserequest']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="course_requests.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone', 'Message', 'Date'])
        messages = CustomCourseRequest.objects.all()
        for message in messages:
            writer.writerow([message.name, message.email, message.phone, message.message, message.created_at])
        return response
    

class DeleteCourseRequestView(PermissionRequiredMixin, View):
    '''Delete contact message view'''
    permission_required = ['dashboard.delete_customcourserequest']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        request_id = request.GET.get('request_id')
        custom_request = CustomCourseRequest.objects.filter(id=request_id).first()
        if custom_request:
            custom_request.delete()
            messages.success(request, 'Course Request Deleted Successfully.')
            return redirect('dashboard:course_requests')
        messages.error(request, 'Course Request Not Found.')
        return redirect('dashboard:course_requests')