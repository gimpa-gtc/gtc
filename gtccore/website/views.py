from django.shortcuts import render
from django.views import View


class HomeView(View):
    '''Home page view.'''
    template = 'website/index.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)
