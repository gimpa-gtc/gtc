import csv

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from dashboard.forms import FacilitatorForm
from dashboard.models import Facilitator


class FacilitorsView(View):
    template = 'dashboard/pages/facilitors.html'

    def get(self, request):
        query = request.GET.get('query')
        if query:
            facilitator = Facilitator.objects.filter(
                Q(name__icontains=query) | 
                Q(title__icontains=query) | 
                Q(specialization__icontains=query)).order_by('-created_at') # noqa
        else:
            facilitator = Facilitator.objects.all().order_by('-created_at')
        context ={
            'facilitator': facilitator
        }
        return render(request, self.template, context)
    

class CreateUpdateFacilitatorView(View):
    '''Create or update facilitator'''
    template = 'dashboard/pages/create-update-facilitator.html'

    def get(self, request):
        facilitator_id = request.GET.get('facilitator_id')
        facilitator = Facilitator.objects.filter(id=facilitator_id).first()
        context = {
            'facilitator': facilitator
        }
        return render(request, self.template, context)

    def post(self, request):
        facilitator_id = request.POST.get('facilitator_id')
        try:
            facilitator_id = int(facilitator_id)
        except:
            facilitator_id = None

        facilitator = Facilitator.objects.filter(id=facilitator_id).first()
        form = FacilitatorForm(request.POST, request.FILES, instance=facilitator)
        if form.is_valid():
            facilitator = form.save()
            if facilitator_id is not None:
                messages.success(request, 'Facilitator Updated Successfully')
            messages.success(request, 'Facilitator Created Successfully')
        redirect_url = reverse('dashboard:create_update_facilitator') + '?facilitator_id=' + str(facilitator.id)
        return redirect(redirect_url)


class DownloadFacilitatorsView(View):
    '''Download facilitators as csv'''
    def get(self, request):
        facilitators = Facilitator.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="facilitators.csv"'
        writer = csv.writer(response)
        writer.writerow(['name', 'title', 'image', 'specialization', 'created_at']) # noqa
        for facilitator in facilitators:
            writer.writerow([facilitator.name, facilitator.title, facilitator.image, facilitator.specialization, facilitator.created_at])
        return response