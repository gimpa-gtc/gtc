from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from accounts.manager import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    prefered_notification_email = models.EmailField(max_length=255, blank=True, null=True)  # noqa
    prefered_notification_phone = models.CharField(max_length=20, blank=True, null=True)  # noqa

    profile_pic = models.ImageField(upload_to='profile', blank=True, null=True)  # noqa

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name if self.name else self.email # noqa

    class Meta:
        db_table = 'user'


class UserLog(models.Model):
    '''User activity log.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    pre_object = models.TextField(blank=True, null=True)
    post_object = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email + ": " + self.action

    class Meta:
        db_table = 'user_log'