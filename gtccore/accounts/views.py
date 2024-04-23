from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View

from accounts.models import User


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

        # check if user has failed to login more than 3 times
        check_user = User.objects.filter(email=username).first()

        # check if the user is suspended
        if check_user and check_user.is_active is False:
            messages.info(request, 'Account Suspended! Please Contact Support.')
            return render(request, self.template_name)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # reset the login attempt
            if check_user:
                check_user.failed_login_attempt = 0
                check_user.save()
            messages.success(request, f'Successfully logged in as {username}')
            return redirect('dashboard:dashboard')
        else:
            # update the login attempt
            if check_user:
                check_user.failed_login_attempt += 1
                # suspend the account if the user has failed to login more than 3 times
                if check_user.failed_login_attempt >= 3:
                    check_user.is_active = False
                check_user.save()
            messages.info(request, 'Invalid Username or Password')
            return render(request, self.template_name)
        

class LogoutView(View):
    '''Logout view'''
    def get(self, request):
        '''Handles GET requests'''
        logout(request)
        return redirect('accounts:login')