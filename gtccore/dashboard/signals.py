from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Application, Applicant


@receiver(post_save, sender=Application)
def extract_applicant(sender, instance, created, **kwargs):
    email = instance.email
    phone = instance.phone

    applicant = Applicant.objects.filter(email=email, phone=phone).first()
    if applicant is not None:
        pass
    else:
        Applicant.objects.create(
            email=instance.email,
            phone=instance.phone,
            name=instance.name
        )