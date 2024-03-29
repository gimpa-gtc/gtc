from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    '''manages User account creation'''

    def create_user(self, email, password, name='-', **kwargs):
        user = self.model(email=email, password=password,
                          name=name, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, name='-', **kwargs):
        user = self.create_user(
            email,  password, name='-', **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
