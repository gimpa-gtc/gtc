from django.shortcuts import render
from django.views import View

from accounts.models import User


class UserListView(View):
    template = 'dashboard/pages/users.html'

    def get(self, request):
        users = User.objects.all().order_by('-created_at')
        context ={
            'users': users
        }
        return render(request, self.template, context)