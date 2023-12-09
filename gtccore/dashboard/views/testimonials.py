import csv

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from dashboard.models import Testimonial

class TestimonialsView(View):
    template = 'dashboard/pages/testimonials.html'

    def get(self, request):
        query = request.GET.get('query')
        if query:
            testimonials = Testimonial.objects.filter(
                Q(name__icontains=query) | 
                Q(company__icontains=query) | 
                Q(content__icontains=query)).order_by('-created_at') # noqa
        else:
            testimonials = Testimonial.objects.all().order_by('-created_at')
        context ={
            'testimonials': testimonials
        }
        return render(request, self.template, context)

class CreateUpdateTestimonialView(View):
    template = 'dashboard/pages/create-update-testimonial.html'

    def get(self, request):
        testimonial_id = request.GET.get('testimonial_id')
        testimonial = None
        if testimonial_id:
            testimonial = Testimonial.objects.filter(id=testimonial_id).first()
        context = {
                'testimonial': testimonial
            }
        return render(request, self.template, context)

    def post(self, request):
        name = request.POST.get('name')
        company = request.POST.get('company')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        testimonial_id = request.POST.get('testimonial_id')
        if testimonial_id:
            testimonial = Testimonial.objects.get(pk=testimonial_id)
            testimonial.name = name
            testimonial.company = company
            testimonial.content = content
            if image:
                testimonial.image = image
            testimonial.save()
            messages.success(request, 'Testimonial updated successfully')
        else:
            testimonial = Testimonial.objects.create(
                name=name,
                company=company,
                content=content,
                image=image
            )
            messages.success(request, 'Testimonial created successfully')
        return redirect(reverse('dashboard:testimonials'))
    
class DeleteTestimonialView(View):
    def get(self, request):
        testimonial_id = request.GET.get('testimonial_id')
        testimonial = Testimonial.objects.get(pk=testimonial_id)
        testimonial.delete()
        messages.success(request, 'Testimonial deleted successfully')
        return redirect(reverse('dashboard:testimonials'))