import csv
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.db.models import Q
from accounts.models import User


class UsersView(View):
    template = 'dashboard/pages/users.html'

    def get(self, request):
        query = request.GET.get('query')
        if query:
            users = User.objects.filter(
                Q(name__icontains=query) | 
                Q(email__icontains=query) | 
                Q(phone__icontains=query)).order_by('-created_at') # noqa
        else:
            users = User.objects.all().order_by('-created_at')
        context ={
            'users': users
        }
        return render(request, self.template, context)
    

class CreateUpdateUser(View):
    '''Create or update user'''
    template = 'dashboard/pages/create-update-user.html'

    def get(self, request):
        user_id = request.GET.get('user_id')
        user = User.objects.filter(id=user_id).first()
        context = {
            'user': user
        }
        return render(request, self.template, context)

    def post(self, request):
        user_id = request.POST.get('user_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        status = request.POST.get('status')
        try:
            user_id = int(user_id)
        except:
            user_id = None

        user = User.objects.filter(id=user_id).first()
        if user:
            # only update if user exists and attributes are not empty
            user.name = name if name else user.name
            user.email = email if email else user.email
            user.phone = phone if phone else user.phone
            user.role = role if role else user.role
            user.status = status if status else user.status
            user.save()
        else:
            try:
                user = User.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    is_staff=role == 'staff',
                    is_superuser=role == 'superuser',
                    is_active=status == 'active'
                )
            except Exception as e:
                user = None
                messages.error(request, f'Error: {e}')
                return redirect('dashboard:create_update_user')
            messages.success(request, 'User Created Successfully')
        redirect_url = reverse('dashboard:create_update_user') + '?user_id=' + str(user.id)
        return redirect(redirect_url)


class UpdateUserProfilePicView(View):
    '''Update user profile picture'''
    def get(self, request):
        return redirect('dashboard:users')
    
    def post(self, request):
        user_id = request.POST.get('user_id')
        profile_pic = request.FILES.get('profile_pic')
        user = User.objects.filter(id=user_id).first()
        if user:
            user.profile_pic = profile_pic
            user.save()
            messages.success(request, 'Profile Picture Updated Successfully')
            return redirect('dashboard:users')
        else:
            messages.error(request, 'User Not Found')
            return redirect('dashboard:users')


class DownloadUsersView(View):
    '''Download users as csv'''
    def get(self, request):
        users = User.objects.all()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'
        writer = csv.writer(response)
        writer.writerow(['primary_key', 'name', 'email', 'phone', 'is_staff', 'is_superuser', 'is_active', 'created_at']) # noqa
        for user in users:
            writer.writerow([user.id, user.name, user.email, user.phone, user.is_staff, user.is_superuser, user.is_active, user.created_at])
        return response