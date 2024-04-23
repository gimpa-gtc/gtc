import csv
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from dashboard.forms import PaymentForm
from django.contrib import messages
from django.utils.decorators import method_decorator

from dashboard.models import Application, Payment
from gtccore.library.decorators import StaffLoginRequired
from gtccore.library.logs import log_user_activity


class PaymentsView(PermissionRequiredMixin, View):
    template = 'dashboard/pages/payments.html'
    permission_required = ['dashboard.view_payment']

    @method_decorator(StaffLoginRequired)
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


class CreatePaymentView(PermissionRequiredMixin, View):
    '''Create payment'''
    template = 'dashboard/pages/create-payment.html'
    permission_required = ['dashboard.add_payment']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        application_id = request.GET.get('application_id')
        if application_id:
            application_id = application_id.strip()
        application = Application.objects.filter(application_id=application_id).first() # noqa
        context = {
            'application': application
        }
        return render(request, self.template, context)
    
    @method_decorator(StaffLoginRequired)
    def post(self, request):
        application_id = request.POST.get('application_id')
        application = Application.objects.filter(application_id=application_id).first()
        form = PaymentForm(request.POST, request.FILES or None)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.application = application
            payment.save()
            # log user activity
            log_user_activity(request.user, 'Created payment', None, payment) # noqa
            messages.success(request, 'Payment Created Successfully')
            return redirect('dashboard:payments')
        else:
            for k, v in form.errors.items():
                messages.error(request, f"{k}: {v}")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            

class ApproveDisapprovePaymentView(PermissionRequiredMixin, View):
    '''Approve or disapprove payment'''
    permission_required = ['dashboard.change_payment']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        payment_id = request.GET.get('payment_id')
        payment = Payment.objects.filter(transaction_id=payment_id).first()

        context = {
            'payment': payment
        }
        return render(request, 'dashboard/pages/verify_payment.html', context)

   
    @method_decorator(StaffLoginRequired)
    def post(self, request):
        payment_id = request.POST.get('payment_id')
        payment = Payment.objects.filter(transaction_id=payment_id).first()

        approval_status = request.POST.get('approval_status')
        if approval_status:
            payment.approve()
            # log user activity
            log_user_activity(request.user, 'Approved Payment', None, payment) # noqa
            messages.success(request, 'Payment Approved Successfully')
        else:
            payment.disapprove()
            # log user activity
            log_user_activity(request.user, 'Disapproved Payment', None, payment)
            messages.success(request, 'Payment Disapproved Successfully')
        return redirect('dashboard:payments')

   

class DownloadPaymentsView(PermissionRequiredMixin, View):
    '''Download payments as csv'''
    permission_required = ['dashboard.view_payment']

    @method_decorator(StaffLoginRequired)
    def get(self, request):
        payments = Payment.objects.all().order_by('-id')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="payments.csv"'
        writer = csv.writer(response)
        writer.writerow(['transaction_id', 'application_id', 'applicant', 'amount', 'network', 'number', 'payment_status' ,'status_code', 'status_message', 'created_at']) # noqa
        for payment in payments:
            writer.writerow([payment.transaction_id, payment.application.application_id,payment.application, payment.amount, payment.network, payment.number, payment.get_payment_status(), '_' +payment.status_code, payment.status_message, payment.created_at]) # noqa
        return response