import csv

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator

from dashboard.models import Facilitator
from gtccore.library.decorators import StaffLoginRequired

class TeamsView(View):
    template = 'dashboard/pages/teams.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        query = request.GET.get('query')
        if query:
            teams = Facilitator.objects.filter(
                Q(name__icontains=query) | 
                Q(title__icontains=query) | 
                Q(specialization__icontains=query)).order_by('-created_at') # noqa
        else:
            teams = Facilitator.objects.all().order_by('-created_at')
        context ={
            'teams': teams
        }
        return render(request, self.template, context)
    
class CreateUpdateTeamView(View):
    '''Create or update team'''
    template = 'dashboard/pages/create-update-team.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        team_id = request.GET.get('team_id')
        team = None
        if team_id:
            team = Facilitator.objects.filter(id=team_id).first()
        context = {
                'team': team
            }
        return render(request, self.template, context)

    @method_decorator(StaffLoginRequired)
    def post(self, request):
        name = request.POST.get('name')
        title = request.POST.get('title')
        specialization = request.POST.get('specialization')
        image = request.FILES.get('image')
        print(image)
        team_id = request.POST.get('team_id')
        if team_id:
            facilitator = Facilitator.objects.get(pk=team_id)
            facilitator.name = name
            facilitator.title = title
            facilitator.specialization = specialization
            if image:
                facilitator.image = image
            facilitator.save()
            messages.success(request, 'Facilitator updated successfully')
        else:
            facilitator = Facilitator.objects.create(
                name=name,
                title=title,
                specialization=specialization,
                image=image
            )
            messages.success(request, 'Facilitator created successfully')
        return redirect(reverse('dashboard:teams'))
    
class DownloadTeamsView(View):
    ''' Download teams as csv'''

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="teams.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'title', 'specialization'])
        teams = Facilitator.objects.all()
        for facilitator in teams:
            writer.writerow([facilitator.name, facilitator.title, facilitator.specialization])
        return response
    
class DeleteTeamView(View):
    '''Delete team'''

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        team_id = request.GET.get('team_id')
        facilitator = Facilitator.objects.get(pk=team_id)
        facilitator.delete()
        messages.success(request, 'Facilitator deleted successfully')
        return redirect(reverse('dashboard:teams'))
    


class DeleteTeamView(View):
    '''Delete team'''

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        member_id = request.GET.get('member_id')
        member = Facilitator.objects.filter(id=member_id).first()
        if member:
            member.delete()
            messages.success(request, 'Member Deleted Successfully.')
            return redirect('dashboard:teams')
        messages.error(request, 'Member Does Not Exist.')
        return redirect('dashboard:teams')