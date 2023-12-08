from django.shortcuts import render
from django.views import View


class InvoiceListView(View):
    template = 'dashboard/pages/invoices.html'

    def get(self, request):
        context ={}
        return render(request, self.template, context)