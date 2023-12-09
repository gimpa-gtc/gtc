from django.shortcuts import render
from django.views import View


class SettingsView(View):
    template = 'dashboard/pages/settings.html'

    def get(self, request):
        user = request.user
        context ={
            'user': user
        }
        return render(request, self.template, context)
    

class PreferenceSettingsView(View):
    template = 'dashboard/pages/preference-settings.html'

    def get(self, request):
        user = request.user
        context = {
            'user': user
        }
        return render(request, self.template, context)
    

class PasswordResetView(View):
    template = 'dashboard/pages/password-reset.html'

    def get(self, request):
        user = request.user
        context ={
            'user': user
        }
        return render(request, self.template, context)
    

