from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator

from gtccore.library.decorators import StaffLoginRequired


class UserProfileView(View):
    '''User profile view'''
    template = 'dashboard/pages/profile.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        context ={}
        return render(request, self.template, context)