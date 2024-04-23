from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from gtccore.library.decorators import StaffLoginRequired


class GroupsView(PermissionRequiredMixin, View):
    '''View for managing user groups and permissions in the system'''
    template = 'dashboard/pages/groups.html'
    permission_required = ['auth.view_group']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        query = request.GET.get('query')
        groups = Group.objects.all().order_by('name')
        if query:
            groups = Group.objects.filter(
                Q(name__icontains=query)
            ).order_by('name')
        context = {
            'groups': groups
        }
        return render(request, self.template, context)
    

class CreateUpdateGroupView(PermissionRequiredMixin, View):
    '''View for creating and updating user groups in the system'''
    template = 'dashboard/pages/create_update_group.html'
    permission_required = ['auth.add_group', 'auth.change_group']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        group_id = request.GET.get('group_id')
        permissions = Permission.objects.all().order_by('name')
        group = Group.objects.filter(id=group_id).first()
        context = {
            'group': group,
            'permissions': permissions
        }
        return render(request, self.template, context)

    @method_decorator(StaffLoginRequired)
    def post(self, request):
        group_id = request.POST.get('group_id') or None
        group = Group.objects.filter(id=group_id).first()
        group_name = request.POST.get('name')
        if group:
            group.name = group_name
            group.save()
            messages.success(request, 'Group Updated Successfully')
        else:
            group = Group.objects.create(name=group_name)
            messages.success(request, f'{group.name.upper()} Group Created Successfully')  # noqa
        return redirect('dashboard:groups')
    

class UpdatePermissionsToGroupView(PermissionRequiredMixin, View):
    '''CBV for updating permissions to a group'''
    template = 'dashboard/pages/update_permissions.html'
    permission_required = ['auth.change_group']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        group = request.GET.get('group_id') or None
        group = Group.objects.filter(id=group).first()
        if group:
            permissions = Permission.objects.all().order_by('name')
            saved_permissions = group.permissions.all()
            context = {
                'group': group,
                'permissions': permissions,
                'saved_permissions': saved_permissions,
            }
            return render(request, self.template, context)  # noqa
        messages.info(request, 'Group Does Not Exist')
        return redirect('dashboard:groups')

    @method_decorator(StaffLoginRequired)
    def post(self, request):
        group_id = request.POST.get('group_id') or None
        group = Group.objects.filter(id=group_id).first()
        group_permissions = request.POST.getlist('permissions')
        if group:
            group.permissions.clear()
            for permission in group_permissions:
                permission = Permission.objects.filter(id=permission).first()
                group.permissions.add(permission)
            group.save()
            messages.success(request, 'Group Permissions Updated Successfully')  # noqa
        else:
            messages.info(request, 'Group does not exist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteGroupView(PermissionRequiredMixin, View):
    '''CBV for deleting a group'''
    permission_required = ['auth.delete_group']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        group_id = request.GET.get('group_id') or None
        group = Group.objects.filter(id=group_id).first()
        if group:
            group.delete()
            messages.success(request, 'Group Deleted Successfully')
        else:
            messages.error(request, 'Group Does Not Exist')
        return redirect('dashboard:groups')