from django.db.models import Sum
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.models import (Admission, Applicant, Application, Course,
                              CourseCategory, Payment)
from gtccore.library.decorators import StaffLoginRequired


class DashboardView(View):
    template = 'dashboard/pages/dashboard.html'

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        # totals
        total_applications = Application.objects.all().count()
        total_applicants = Applicant.objects.all().count()
        total_payments = Payment.objects.all().count()
        total_admissions = Admission.objects.all().count()
        total_courses = Course.objects.all().count()
        total_categories = CourseCategory.objects.all().count()
        successful_payments = Payment.objects.filter(status_code='000')
        payements_received = successful_payments.aggregate(Sum('amount'))
        context ={
            'total_applications': total_applications,
            'total_applicants': total_applicants,
            'total_payments': total_payments,
            'total_admissions': total_admissions,
            'total_courses': total_courses,
            'total_categories': total_categories,
            'payements_received': payements_received['amount__sum'],
        }
        return render(request, self.template, context)