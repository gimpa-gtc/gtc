from datetime import timezone

from django.db import models

from gtccore.library.constants import (ApplicationStatus, PaymentMode,  # noqa
                                       PaymentStatus)

'''
List of models:
1. User
2. Application
3. Admission
4. Course
5. Course Category
6. Payment
7. invoice
'''

class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='Course Categories'

    def __str__(self):
        return self.name
    

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
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
    created_at = models.DateTimeField(auto_now_add=True)

    def is_active(self):
        '''Returns True if the course is active'''
        return self.end_date > timezone.now().date()

    def __str__(self):
        return self.name
    
import random
import string


class Application(models.Model):
    def generate_application_id() -> str:
        '''Generates a unique application id'''
        return 'GTC-AP-'.join(random.choices(string.digits, k=7))
    
    # choices for payment mode: Online, Bank
    PAYMENT_STATUS = [(status.name, status.value) for status in PaymentStatus] #noqa
    
    # choices for payment status: Pending, Paid
    PAYMENT_MODE = [(mode.name, mode.value) for mode in PaymentMode] #noqa

    # choices for application status: Pending, Approved, Rejected
    APPLICATION_STATUS = [(status.name, status.value) for status in ApplicationStatus] #noqa

    application_id = models.CharField(max_length=15, default=generate_application_id, unique=True) #noqa
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    application_status = models.CharField(max_length=20, default='pending', choices=APPLICATION_STATUS) #noqa
    payment_mode = models.CharField(max_length=20, default='pending', choices=PAYMENT_MODE) #noqa
    payment_status = models.CharField(max_length=20, default='pending', choices=PAYMENT_STATUS) #noqa
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name