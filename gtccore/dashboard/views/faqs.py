import csv
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator

from dashboard.models import Faq
from gtccore.library.decorators import StaffLoginRequired

class FAQsView(PermissionRequiredMixin, View):
    template = 'dashboard/pages/faqs.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        query = request.GET.get('query')
        if query:
            faqs = Faq.objects.filter(
                Q(question__icontains=query) | 
                Q(answer__icontains=query)).order_by('-created_at') # noqa
        else:
            faqs = Faq.objects.all().order_by('-created_at')
        context ={
            'faqs': faqs
        }
        return render(request, self.template, context)
    
class CreateUpdateFAQView(PermissionRequiredMixin, View):
    template = 'dashboard/pages/create-update-faq.html'
    permission_required = [
        'dashboard.add_faq',
        'dashboard.change_faq'
    ]

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        faq_id = request.GET.get('faq_id')
        faq = None
        if faq_id:
            faq = Faq.objects.filter(id=faq_id).first()
        context = {
                'faq': faq
            }
        return render(request, self.template, context)

    @method_decorator(StaffLoginRequired)
    def post(self, request):
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        faq_id = request.POST.get('faq_id')
        if faq_id:
            faq = Faq.objects.filter(pk=faq_id).first()
            faq.question = question
            faq.answer = answer
            faq.save()
            messages.success(request, 'FAQ updated successfully')
        else:
            faq = Faq.objects.create(
                question=question,
                answer=answer
            )
            messages.success(request, 'FAQ created successfully')
        return redirect(reverse('dashboard:faqs'))
    
class DeleteFAQView(PermissionRequiredMixin, View):
    '''Delete FAQ view'''
    permission_required = ['dashboard.delete_faq']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        faq_id = request.GET.get('faq_id')
        faq = Faq.objects.filter(id=faq_id).first()
        if faq:
            faq.delete()
            messages.success(request, 'FAQ Deleted Successfully')
            return redirect(reverse('dashboard:faqs'))
        else:
            messages.error(request, 'FAQ Not Found')
            return redirect(reverse('dashboard:faqs'))