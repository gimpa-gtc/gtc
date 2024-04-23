import csv
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.decorators import method_decorator

from dashboard.models import Applicant, Notification
from dashboard.forms import NotificationForm
from gtccore.library.decorators import StaffLoginRequired

class NotificationsView(View):
    '''Notifications view'''
    template = 'dashboard/pages/notifications.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        query = request.GET.get('query')
        notifications = Notification.objects.all().order_by('-id')
        if query:
            notifications = Notification.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            ).order_by('-id')
        context ={
            'notifications': notifications
        }
        return render(request, self.template, context)
    
class CreateUpdateNotificationView(View):
    '''Create and update notification view'''
    template = 'dashboard/pages/create-update-notification.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        notification_id = request.GET.get('notification_id')
        notification = None
        if notification_id:
            notification = Notification.objects.filter(id=notification_id).first()
        context = {
            'notification': notification
        }
        return render(request, self.template, context)
    
    @method_decorator(StaffLoginRequired)
    def post(self, request):
        notification_id = request.POST.get('notification_id')
        notification = None
        if notification_id:
            notification = Notification.objects.filter(id=notification_id).first()
        form = NotificationForm(request.POST, instance=notification)
        if form.is_valid():
            form.save()
            if notification is None:
                messages.success(request, 'Notification Created Successfully.')
                return redirect('dashboard:notifications')
            messages.success(request, 'Notification Updated Successfully.')
            return redirect('dashboard:notifications')
        else:
            for k, v in form.errors.items():
                messages.error(request, f"{k}: {v}")
                return redirect('dashboard:notifications')


class BroadcastNotificationView(View):
    '''Broadcast notification to all users'''

    template = 'dashboard/pages/broadcast-notification.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        notification_id = request.GET.get('notification_id')
        notification = Notification.objects.filter(id=notification_id).first()
        applicants = Applicant.objects.count()
        context = {
            'notification': notification,
            'applicants': applicants
        }
        return render(request, self.template, context)

    @method_decorator(StaffLoginRequired)
    def post(self, request):
        notification_id = request.POST.get('notification_id')
        notification_type = request.POST.get('type')
        notification = Notification.objects.filter(id=notification_id).first()
        if notification:
            sent = notification.broadcast(notification_type)
            if sent:
                messages.success(request, f'{notification_type.upper()} Notification Broadcasted Successfully.')
            else:
                messages.error(request, f'Error Broadcasting {notification_type.upper()} Notification.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        messages.error(request, 'Notification Not Found.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DownloadNotificationView(View):
    '''Download notifications as csv'''

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        notifications = Notification.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="notifications.csv"'
        writer = csv.writer(response)
        writer.writerow(['title', 'content', 'created_at']) # noqa
        for notification in notifications:
            writer.writerow([notification.title, notification.content, notification.created_at])
        return response
    

class DeleteNotificationView(View):
    '''Delete notification'''

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        notification_id = request.GET.get('notification_id')
        notification = Notification.objects.filter(id=notification_id).first()
        if notification:
            notification.delete()
            messages.success(request, 'Notification Deleted Successfully.')
            return redirect('dashboard:notifications')
        messages.error(request, 'Notification Not Found.')
        return redirect('dashboard:notifications')