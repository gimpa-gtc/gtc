from django.shortcuts import render
from django.views import View


class UserProfileView(View):
    template = 'dashboard/pages/profile.html'

    def get(self, request):
        context ={}
        return render(request, self.template, context)