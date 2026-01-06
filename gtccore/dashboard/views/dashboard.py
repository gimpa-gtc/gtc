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

        # Applications and Admissions by month for the past 12 months
        from django.utils import timezone
        from django.db.models.functions import TruncMonth
        from django.db import models
        from datetime import timedelta
        import calendar


        now = timezone.now()
        # Get the first day of the current month
        first_of_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        months = []
        month_labels = []
        for i in range(12):
            # Go back i months from current month
            year = first_of_this_month.year
            month = first_of_this_month.month - i
            while month <= 0:
                month += 12
                year -= 1
            dt = first_of_this_month.replace(year=year, month=month)
            months.append(dt)
            month_labels.append(dt.strftime('%b %Y'))
        months = list(reversed(months))
        month_labels = list(reversed(month_labels))

        # Applications by month

        applications_by_month = Application.objects.filter(
            created_at__gte=months[0],
            created_at__lte=now
        ).annotate(month=TruncMonth('created_at')).values('month').order_by('month').annotate(count=models.Count('id'))

        # Admissions by month

        admissions_by_month = Admission.objects.filter(
            created_at__gte=months[0],
            created_at__lte=now
        ).annotate(month=TruncMonth('created_at')).values('month').order_by('month').annotate(count=models.Count('id'))

        # Map counts to months
        app_counts = {a['month'].strftime('%b %Y'): a['count'] for a in applications_by_month}
        adm_counts = {a['month'].strftime('%b %Y'): a['count'] for a in admissions_by_month}
        applications_data = [app_counts.get(label, 0) for label in month_labels]
        admissions_data = [adm_counts.get(label, 0) for label in month_labels]

        context ={
            'total_applications': total_applications,
            'total_applicants': total_applicants,
            'total_payments': total_payments,
            'total_admissions': total_admissions,
            'total_courses': total_courses,
            'total_categories': total_categories,
            'payements_received': payements_received['amount__sum'],
            'applications_analysis': {
                'labels': month_labels,
                'applications': applications_data,
                'admissions': admissions_data,
            },
        }

        print(f"Dashboard context: {context}")
        return render(request, self.template, context)