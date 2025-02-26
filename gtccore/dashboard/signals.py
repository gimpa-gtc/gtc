import random

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User
from gtccore.library.services import send_mail, send_sms
from gtccore.settings import SENDER_ID

from .models import Admission, Applicant, Application, CustomCourseRequest


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
                name=instance.name,
                dob=instance.dob,
                box_address=instance.box_address,
            )
        except Exception as er:
            print(f"Error: {er}")
        return True


@receiver(post_save, sender=CustomCourseRequest)
def notify_custom_course_requester(sender, instance, created, **kwargs):
    '''Send the notification to applicants upon saving of notification'''
    if not created:
        return
    msg = f"Hello {instance.name}, \nYour request for a custom course has been received. We will get back to you shortly."
    send_sms(SENDER_ID, msg, [str(instance.phone)])
    return True


@receiver(post_save, sender=Application)
def notify_applicant(sender, instance, created, **kwargs):
    '''Send the notification to applicants when they start an application'''
    if not(created):
        return
    msg = f"Hello {instance.name}, \nYour Application has been received. We will get back to you shortly.\n\nApplication ID: {instance.application_id}\n\nThank you for choosing GIMPA Training & Consulting."
    send_sms(SENDER_ID, msg, [str(instance.phone)])
    return True

@receiver(post_save, sender=Application)
def notify_coordinator(sender, instance, created, **kwargs):
    '''Notify the course coordinator when new application is opened'''
    if not(created):
        return
    coordinator_email = instance.course.category.coordinator_email
    coordinator_phone = instance.course.category.coordinator_phone
    msg = f"Dear Coordinator, \nA new application has been received for the course {instance.course.title}. \n\nApplicant: {instance.name} \nEmail: {instance.email} \nPhone: {instance.phone} \n\nApplication ID: {instance.application_id}\n\nThanks!"
    if coordinator_phone is not None and coordinator_phone != '':
        send_sms(SENDER_ID, msg, [str(coordinator_phone)])

    if coordinator_email is not None and coordinator_email != '':
        send_mail([coordinator_email], 'New Application', msg)
    return True

@receiver(post_save, sender=Application)
def notify_team_on_new_application(sender, instance, created, **kwargs):
    '''Notify the team via their unified official mail'''
    if not(created):
        return
    msg = f"Hi Team!, \nA new application has been received for the course {instance.course.title}. \n\nApplicant: {instance.name} \nEmail: {instance.email} \nPhone: {instance.phone} \n\nApplication ID: {instance.application_id}\n\nThanks!"
    send_mail(["trainingandconsulting@gimpa.edu.gh"], 'New Application', msg)
    return True

@receiver(post_save, sender=Admission)
def notify_applicant_on_admission(sender, instance, created, **kwargs):
    '''Notify the applicant when their application is approved/rejected'''
    if not(created):
        return
    msg = f"Congratulations!\n\nDear {instance.application.name}, \nYour Application to study {instance.application.course.title} is successful! \n\nDownload your admission letter here for more details:\nhttps://gtc.gimpa.edu.gh/application/status/?application_id={instance.application.application_id} \n\nThank you for choosing GIMPA Training & Consulting."
    send_sms(SENDER_ID, msg, [str(instance.application.phone)])
    return True

@receiver(post_save, sender=CustomCourseRequest)
def notify_custom_course_admin(sender, instance, created, **kwargs):
    '''Send the notification to applicants upon saving of notification'''
    if not created:
        return
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
    msg = f"Hello {instance.name}, \nYour GTC staff account has been created. \n\nKindly login with the credentials below: \n\nUsername: {instance.email} \nPassword: {password}.\nURL: https://gtc.gimpa.edu.gh/login/\n\nThanks!"
    send_sms(SENDER_ID, msg, [str(instance.phone)])
    return True