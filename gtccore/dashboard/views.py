from django.shortcuts import render
from django.views import View


class DashboardView(View):
    template = 'dashboard/dashboard.html'

    def get(self, request):
        context ={}
        return render(request, self.template, context)