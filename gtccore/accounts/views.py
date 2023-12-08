from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View


class LoginView(View):
    '''Login view'''
    template_name = 'accounts/login.html'

    def get(self, request):
        '''Handles GET requests'''
        return render(request, self.template_name)

    def post(self, request):
        '''Handles POST requests'''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Successfully logged in as {username}')
            return redirect('dashboard:dashboard')
        else:
            messages.info(request, 'Invalid username or password')
            return render(request, self.template_name)
        

class LogoutView(View):
    '''Logout view'''
    def get(self, request):
        '''Handles GET requests'''
        logout(request)
        return redirect('accounts:login')