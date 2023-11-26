from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Application, Applicant, Notification
from gtccore.libary.services import send_sms
from gtccore.settings import SENDER_ID, ARKESEL_API_KEY


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


@receiver(post_save, sender=Notification)
def notify_applicants(sender, instance, created, **kwargs):
    '''Send the notification to applicants upon saving of notification'''
    applicants = Applicant.objects.all()
    msg = f"{instance.title} \n{instance.content}"
    numbers = [str(applicant.phone) for applicant in applicants]
    emails = [str(applicant.email) for applicant in applicants]

    send_sms(SENDER_ID, msg, numbers)
    return True
