import array

import requests
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from gtccore import settings


def send_sms(sender: str, message: str, recipients: array.array):
    '''Sends an SMS to the specified recipients'''
    header = {"api-key": settings.ARKESEL_API_KEY, 'Content-Type': 'application/json',
              'Accept': 'application/json'}
    SEND_SMS_URL = "https://sms.arkesel.com/api/v2/sms/send"
    payload = {
        "sender": sender,
        "message": message,
        "recipients": recipients
    } 
    try:
        response = requests.post(SEND_SMS_URL, headers=header, json=payload)
    except Exception as e:
        print(f"Error: {e}")
        return False
    else:
        print(response.json())
        return response.json()
    
def send_mail(receipients: array.array, subject: str, message: str, instance=None):
    subject = 'GTC Support'
    from_email = None
    template = "dashboard/notifications/application_notification.html"
    context = {"instance": instance, "message": message}
    html_content = render_to_string(template, context)
    email = EmailMultiAlternatives(subject, '', from_email, receipients)
    email.attach_alternative(html_content, 'text/html')
    try:
        email.send()
        print('Email sent successfully.')
    except Exception as e:
        print(f'Error: {e}')
        return False
    return True