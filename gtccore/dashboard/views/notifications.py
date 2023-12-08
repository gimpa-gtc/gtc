import csv

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from dashboard.models import Notification
from dashboard.forms import NotificationForm

class NotificationsView(View):
    '''Notifications view'''
    template = 'dashboard/pages/notifications.html'

    def get(self, request):
        query = request.GET.get('query')
        notifications = Notification.objects.all().order_by('-id')
        if query:
            notifications = Notification.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(created_at__icontains=query)
            ).order_by('-id')
        context ={
            'notifications': notifications
        }
        return render(request, self.template, context)
    
class CreateUpdateNotificationView(View):
    '''Create and update notification view'''
    template = 'dashboard/pages/create-update-notification.html'

    def get(self, request):
        notification_id = request.GET.get('notification_id')
        notification = None
        if notification_id:
            notification = Notification.objects.filter(id=notification_id).first()
        context = {
            'notification': notification
        }
        return render(request, self.template, context)
    
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