from datetime import timezone

from django.db import models

from gtccore.library.constants import (ApplicationStatus, PaymentMode,  # noqa
                                       PaymentStatus)

import random
import string


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
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.IntegerField(default=0)
    duration = models.CharField(max_length=100, default='')
    class_days = models.CharField(max_length=100, default='')
    class_time = models.TimeField()
    teachers = models.CharField(max_length=100, default='')
    student_capacity = models.IntegerField(default=1)
    requirements = models.TextField(default='None')
    syllabus = models.TextField(default='None')
    thumbnail = models.ImageField(upload_to='courses', null=True, blank=True) #noqa
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
    application = models.OneToOneField(Application, on_delete=models.CASCADE) #noqa
    amount = models.IntegerField(default=0)
    network = models.CharField(max_length=5)
    number = models.CharField(max_length=10)
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

    def __str__(self) -> str:
        return self.name


class CustomCourseRequest(models.Model):
    '''Custom course request model'''
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    course = models.CharField(max_length=100)
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
    

class Facilitator(models.Model):
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

    def __str__(self) -> str:
        return self.name
    

class Image(models.Model):
    '''Image model'''
    image = models.ImageField(upload_to='gallery')
    category = models.ForeignKey(ImageCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.image.name