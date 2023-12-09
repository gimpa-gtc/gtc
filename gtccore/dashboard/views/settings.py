from django.shortcuts import render
from django.views import View


class SettingsView(View):
    template = 'dashboard/pages/settings.html'

    def get(self, request):
        context ={}
        return render(request, self.template, context)
    

class PreferenceSettingsView(View):
    template = 'dashboard/pages/preference-settings.html'

    def get(self, request):
        context ={}
        return render(request, self.template, context)
    

