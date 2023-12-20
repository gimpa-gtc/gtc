from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login


class SettingsView(View):
    template = 'dashboard/pages/settings.html'

    def get(self, request):
        user = request.user
        context ={
            'user': user
        }
        return render(request, self.template, context)
    
    def post(self, request):
        user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        if name:
            user.name = name
        if email:
            user.email = email
        if phone:
            user.phone = phone
        user.save()
        messages.success(request, 'Profile Updated Successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

class PreferenceSettingsView(View):
    template = 'dashboard/pages/preference-settings.html'

    def get(self, request):
        user = request.user
        context = {
            'user': user
        }
        return render(request, self.template, context)
    
    def post(self, request):
        user = request.user
        prefered_email = request.POST.get('prefered_email')
        prefered_phone = request.POST.get('prefered_phone')
        user.prefered_notification_email = prefered_email if prefered_email else None
        user.prefered_notification_phone = prefered_phone if prefered_phone else None
        user.save()
        messages.success(request, 'Preferences Updated Successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ChangeProfilePicView(View):

    def get(self, request):
        return redirect('dashboard:settings')
    
    def post(self, request):
        user = request.user
        profile_pic = request.FILES.get('profile_pic')
        if not profile_pic:
            messages.error(request, 'Please Select a Profile Picture')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        user.profile_pic = profile_pic
        user.save()
        messages.success(request, 'Profile Updated Successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PasswordResetView(View):
    template = 'dashboard/pages/password-reset.html'

    def get(self, request):
        user = request.user
        context ={
            'user': user
        }
        return render(request, self.template, context)
    
    def post(self, request):
        user = request.user
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, 'Passwords Do Not Match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            user.set_password(password1)
            user.save()
            # re-authenticate user
            authenticated_user = authenticate(request, username=user.email, password=password1)
            if authenticated_user:
                login(request, authenticated_user)
                messages.success(request, 'Password Reset Successfully')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'Password Reset Failed')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

