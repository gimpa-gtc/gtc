from django.shortcuts import render
from django.views import View

from dashboard.models import Payment


class PaymentsView(View):
    template = 'dashboard/pages/payments.html'

    def get(self, request):
        payments = Payment.objects.all().order_by('-id')
        context ={
            'payments': payments
        }
        return render(request, self.template, context)