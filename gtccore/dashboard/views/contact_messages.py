import csv

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from dashboard.models import Contact

class ContactMessagesView(View):
    '''Contact messages view'''
    template = 'dashboard/pages/contact_messages.html'

    def get(self, request):
        query = request.GET.get('query')
        contact_messages = Contact.objects.all().order_by('-id')
        print(contact_messages)
        if query:
            contact_messages = Contact.objects.filter(
                Q(name__icontains=query)
            ).order_by('-id')
        context ={
            'contact_messages': contact_messages
        }
        return render(request, self.template, context)

class ReplyMessageView(View):
    '''Reply message view'''
    template = 'dashboard/pages/reply_message.html'

    def get(self, request):
        message_id = request.GET.get('message_id')
        message = Contact.objects.filter(id=message_id).first()
        context = {
            'message': message
        }
        return render(request, self.template, context)
    
    def post(self, request):
        message_id = request.POST.get('message_id')
        message = Contact.objects.filter(id=message_id).first()
        message.reply = request.POST.get('reply')
        message.save()
        messages.success(request, 'Message Replied Successfully.')
        return redirect('dashboard:contact_messages')
    
class DownloadContactMessagesView(View):
    '''Download contact messages view'''
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contact_messages.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Phone', 'Message', 'Date'])
        messages = Contact.objects.all()
        for message in messages:
            writer.writerow([message.name, message.email, message.phone, message.message, message.created_at])
        return response