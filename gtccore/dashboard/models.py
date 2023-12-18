import random
import string

from django.db import models
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from gtccore.library.constants import (ApplicationStatus, PaymentMode,  # noqa
                                       PaymentStatus)
from gtccore.library.services import send_sms
from gtccore.settings import SENDER_ID


class CourseCategory(models.Model):
    '''Course category model'''
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='Course Categories'


    def get_total_courses(self):
        '''Returns the total number of courses in this category'''
        return Course.objects.filter(category=self).count()
    
    def get_active_courses(self):
        '''Returns the total number of active courses in this category'''
        return Course.objects.filter(category=self, end_date__gte=timezone.now().date()).count() #noqa
    
    def get_inactive_courses(self):
        '''Returns the total number of inactive courses in this category'''
        return Course.objects.filter(category=self, end_date__lt=timezone.now().date()).count() #noqa
    
    def get_total_applications(self):
        '''Returns the total number of applications in this category'''
        return Application.objects.filter(course__category=self).count()

    def get_total_admissions(self):
        '''Returns the total number of admissions in this category'''
        return Admission.objects.filter(application__course__category=self).count()

    def __str__(self):
        return self.name
    

class Course(models.Model):
    '''Course model'''
    title = models.CharField(max_length=200)
    description = models.TextField()
    details = models.TextField(default='') #noqa More extensive description
    cohort = models.ForeignKey('Cohort', blank=True, null=True, on_delete=models.CASCADE) #noqa
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, null=True, blank=True) #noqa
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.IntegerField(default=0)
    duration = models.CharField(max_length=100, default='1 MONTH')
    class_days = models.CharField(max_length=100, default='')
    class_time = models.TimeField()
    location = models.CharField(max_length=100, default='GIMPA MAIN CAMPUS')
    student_capacity = models.IntegerField(default=1)
    requirements = models.TextField(default='None')
    syllabus = models.TextField(default='None')
    thumbnail = models.ImageField(upload_to='courses', null=True, blank=True) #noqa
    allows_part_payment = models.BooleanField(default=False)
    requires_certificate = models.BooleanField(default=False)
    certificate = models.FileField(upload_to='certificates', null=True, blank=True) #noqa
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        '''Returns True if the course is active'''
        return self.end_date > timezone.now().date()
    
    def get_total_applications(self):
        '''Returns the total number of applications for this course'''
        return Application.objects.filter(course=self).count()
    
    def get_total_admissions(self):
        '''Returns the total number of admissions for this course'''
        return Admission.objects.filter(application__course=self).count()


    def get_total_comment(self):
        '''gets the total number of comments for that course'''
        return Comment.objects.filter(course=self).count()

    def __str__(self):
        return self.title


class Application(models.Model):
    '''Application model'''
    def generate_application_id() -> str:
        '''Generates a unique application id'''
        sub = 'GTC-AP-'
        return sub + ''.join(random.choices(string.digits, k=7))
    
    # choices for payment mode: Online, Bank
    PAYMENT_STATUS = [(status.name, status.value) for status in PaymentStatus] #noqa
    
    # choices for payment status: PENDING, Paid
    PAYMENT_MODE = [(mode.name, mode.value) for mode in PaymentMode] #noqa

    # choices for application status: PENDING, APPROVED, Rejected
    APPLICATION_STATUS = [(status.name, status.value) for status in ApplicationStatus] #noqa

    application_id = models.CharField(max_length=15, default=generate_application_id, unique=True) #noqa
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True) #noqa
    application_status = models.CharField(max_length=20, default='PENDING', choices=APPLICATION_STATUS) #noqa
    payment_mode = models.CharField(max_length=20, default='ONLINE', choices=PAYMENT_MODE) #noqa
    payment_status = models.CharField(max_length=20, default='PENDING', choices=PAYMENT_STATUS) #noqa
    created_at = models.DateTimeField(auto_now_add=True)


    def payment_color(self):
        '''Returns the color for the payment status'''
        if self.payment_status == 'PENDING':
            return 'secondary'
        elif self.payment_status == 'PAID':
            return 'success'
        else:
            return 'info'
        
    def status_color(self):
        '''Returns the color for the application status'''
        if self.application_status == 'PENDING':
            return 'secondary'
        elif self.application_status == 'APPROVED':
            return 'success'
        else:
            return 'info'

    def __str__(self):
        return self.name
    

class Admission(models.Model):
    '''Admission model'''
    application = models.OneToOneField(Application, on_delete=models.CASCADE) #noqa
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.application.application_id
    

class Payment(models.Model):
    '''Payment model'''
    transaction_id = models.CharField(max_length=100)
    application = models.OneToOneField(Application, on_delete=models.CASCADE, blank=True, null=True) #noqa
    amount = models.IntegerField(default=0)
    network = models.CharField(max_length=5)
    number = models.CharField(max_length=10)
    receipt = models.ImageField(upload_to='receipts', null=True, blank=True) #noqa
    status_code = models.CharField(max_length=20)
    status_message = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Applicant(models.Model):
    '''Applicant model: Extracted from Applications'''
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Notification(models.Model):
    '''Notification model: used to send announcements to applicants'''

    title = models.CharField(max_length=400)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def broadcast(self, btype='sms'):
        '''Broadcasts the notification to all applicants'''
        applicants = Applicant.objects.all()
        phones = [applicant.phone for applicant in applicants]
        emails = [applicant.email for applicant in applicants]
        if btype.lower() == 'sms':
            print('Sending sms to all applicants...')
            msg = f'{self.title}\n{self.content}'
            try:
                send_sms(sender=SENDER_ID, message=msg, recipients=phones)
                print('SMS sent successfully.')
            except Exception as e:
                print(f'Error: {e}')
                return False
            return True
        elif btype.lower() == 'email':
            print('Sending email to all applicants...')
            subject = self.title
            from_email = None
            receipients = ["princesamuelpks@gmail.com"]
            template = "dashboard/notifications/event-notification.html"
            context = {"notification": self}
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
        else:
            print('Invalid broadcast type.')
            return

    def __str__(self) -> str:
        return self.title


class Faq(models.Model):
    '''Frequently asked questions model'''
    question = models.CharField(max_length=400)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.question


class Contact(models.Model):
    '''Contact model'''
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def reply_message(self, msg: str):
        '''Replies the message'''
        subject = 'GTC - Contact Message'
        from_email = None
        receipients = [self.email]
        template = "dashboard/notifications/contact-reply.html"
        context = {"instance": self, "message": msg}
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


    def __str__(self) -> str:
        return self.name


class CustomCourseRequest(models.Model):
    '''Custom course request model'''
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def reply_message(self, msg: str):
        '''Replies the message'''
        subject = 'GTC - Course Request'
        from_email = None
        receipients = [self.email]
        template = "dashboard/notifications/contact-reply.html"
        context = {"instance": self, "message": msg}
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

    def __str__(self) -> str:
        return self.name


class Cohort(models.Model):
    '''Cohort model'''
    name = models.CharField(max_length=100)
    start_month = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Testimonial(models.Model):
    '''Testimonial model'''
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    image = models.ImageField(upload_to='testimonials')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    

class Comment(models.Model):
    '''Comment model'''
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    

class Facilitator(models.Model): #GTC TEAM
    '''Facilitator model'''
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='facilitators')
    specialization = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    

class ImageCategory(models.Model):
    '''Image category model'''
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_images(self):
        '''Returns the total number of images in this category'''
        return Image.objects.filter(category=self).count()

    def __str__(self) -> str:
        return self.name
    

class Image(models.Model):
    '''Image model'''
    image = models.ImageField(upload_to='gallery')
    category = models.ForeignKey(ImageCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.image.name