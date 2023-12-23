import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User

from gtccore.library.services import send_sms
from gtccore.settings import SENDER_ID

from .models import (Admission, Applicant, Application, CustomCourseRequest)


@receiver(post_save, sender=Application)
def extract_applicant(sender, instance, created, **kwargs):
    '''For every saved Application, extract and save the corresponding Applicant'''
    email = instance.email
    phone = instance.phone

    applicant = Applicant.objects.filter(email=email, phone=phone).first()
    if applicant is not None:
        # Applicant already exists
        return
    else:
        try:
            Applicant.objects.create(
                email=instance.email,
                phone=instance.phone,
                name=instance.name
            )
        except Exception as er:
            print(f"Error: {er}")
        return True


@receiver(post_save, sender=CustomCourseRequest)
def notify_custom_course_requester(sender, instance, created, **kwargs):
    '''Send the notification to applicants upon saving of notification'''
    msg = f"Hello {instance.name}, \nYour request for a custom course has been received. We will get back to you shortly."
    send_sms(SENDER_ID, msg, [str(instance.phone)])
    return True


@receiver(post_save, sender=Application)
def notify_applicant(sender, instance, created, **kwargs):
    '''Send the notification to applicants when they start an application'''
    if not(created):
        return
    msg = f"Hello {instance.name}, \nYour Application has been received. We will get back to you shortly.\n\nApplication ID: {instance.application_id}\n\nThank you for choosing Gimpa Training & Consulting."
    send_sms(SENDER_ID, msg, [str(instance.phone)])
    return True



@receiver(post_save, sender=CustomCourseRequest)
def notify_custom_course_admin(sender, instance, created, **kwargs):
    '''Send the notification to applicants upon saving of notification'''
    msg = f"Hello Admin, \nA new request for a custom course has been received. Please check the admin panel for details."
    admins = User.objects.filter(is_staff=True)
    receivers = [str(admin.prefered_notification_phone) if admin.prefered_notification_phone else admin.phone for admin in admins]
    send_sms(SENDER_ID, msg, receivers)
    return True


@receiver(post_save, sender=Application)
def generate_admission(sender, instance, created, **kwargs):
    '''Generate admission for applicant'''
    admission = Admission.objects.filter(application=instance).first()
    approved = instance.application_status == 'APPROVED'
    # Create admission if application is approved and admission is not None
    if approved and admission is None:
        try:
            Admission.objects.create(
                application=instance,
            )
        except Exception as er:
            print(f"Error: {er}")
        return True
    # Delete admission if application is not approved
    if not(approved) and admission is not None:
        admission.delete()
        return True
    

@receiver(post_save, sender=User)
def send_user_password(sender, instance, created, **kwargs):
    '''Send user's password to them upon account creation'''
    if not(created):
        return
    # generate password
    password = str(random.randint(100000, 999999))
    instance.set_password(password)
    instance.save()
    msg = f"Hello {instance.name}, \nYour GTC staff account has been created. \n\nKindly login with the password {password}. "
    send_sms(SENDER_ID, msg, [str(instance.phone)])
    return True