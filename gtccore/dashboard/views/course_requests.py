import csv

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.utils.decorators import method_decorator

from dashboard.models import CustomCourseRequest
from gtccore.library.decorators import StaffLoginRequired

class CourseRequestsView(View):
    '''Contact messages view'''
    template = 'dashboard/pages/course_requests.html'

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

class ReplyCourseRequestView(View):
    '''Reply message view'''
    template = 'dashboard/pages/reply_course_request.html'

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
        custom_request.reply_message(f"{title}\n\n{message}")
        messages.success(request, 'Message Replied Successfully.')
        return redirect('dashboard:course_requests')
    
class DownloadCourseRequestsView(View):
    '''Download contact messages view'''

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