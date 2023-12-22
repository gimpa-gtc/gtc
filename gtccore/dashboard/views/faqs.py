import csv

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from dashboard.models import Faq

class FAQsView(View):
    template = 'dashboard/pages/faqs.html'

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
    
class CreateUpdateFAQView(View):
    template = 'dashboard/pages/create-update-faq.html'

    def get(self, request):
        faq_id = request.GET.get('faq_id')
        faq = None
        if faq_id:
            faq = Faq.objects.filter(id=faq_id).first()
        context = {
                'faq': faq
            }
        return render(request, self.template, context)

    def post(self, request):
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        faq_id = request.POST.get('faq_id')
        if faq_id:
            faq = Faq.objects.get(pk=faq_id)
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
    
class DeleteFAQView(View):
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