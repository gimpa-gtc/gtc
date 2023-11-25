from django.shortcuts import render
from django.views import View


class UserListView(View):
    template = 'dashboard/pages/users.html'

    def get(self, request):
        context ={}
        return render(request, self.template, context)