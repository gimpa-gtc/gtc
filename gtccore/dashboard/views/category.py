from django.shortcuts import render
from django.views import View

class CategoryListView(View):
    template = 'dashboard/pages/category.html'

    def get(self, request):
        context ={}
        return render(request, self.template, context)