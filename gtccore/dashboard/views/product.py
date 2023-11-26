from django.shortcuts import render
from django.views import View


class ProductListView(View):
    template = 'dashboard/pages/product-list.html'

    def get(self, request):
        context ={}
        return render(request, self.template, context)