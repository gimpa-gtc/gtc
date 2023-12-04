from django.shortcuts import render
from django.views import View
from django.db.models import Q
from dashboard.models import Payment


class PaymentsView(View):
    template = 'dashboard/pages/payments.html'

    def get(self, request):
        payments = Payment.objects.all().order_by('-id')
        query = request.GET.get('query')
        if query:
            payments = Payment.objects.filter(
                Q(pyment__transaction_id__icontains=query) | 
                Q(payment__phone__icontains=query) | 
                Q(payment__status_message__icontains=query) | 
                Q(payment__status_code__icontains=query) | 
                Q(payment_network__icontains=query)).order_by('-id') # noqa
        context ={
            'payments': payments
        }
        return render(request, self.template, context)