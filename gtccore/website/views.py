from django.http import FileResponse
from django.shortcuts import render
from django.views import View
from django.db.models import Q
from io import BytesIO

from gtccore.library.services import generate_admission_letter


class HomeView(View):
    '''Home page view.'''
    template = 'website/index.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)


class ContactView(View):
    '''Contact page view.'''
    template = 'website/contact.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)
    

class FaqsView(View):
    '''FAQs page view.'''
    template = 'website/faqs.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)
    

class ApplicationView(View):
    '''Application page view.'''
    template = 'website/application.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)
    

class ApplicationStatusView(View):
    '''Application Status page view.'''
    template = 'website/application_status.html'

    def get(self, request):
        context = {}
        return render(request, self.template, context)
    

class DownloadAdmissionLetterView(View):
    '''Download Admission Letter page view.'''
    template = 'website/download_admission_letter.html'

    def get(self, request):
        pdf = generate_admission_letter()

        # Create a BytesIO buffer to store the PDF content
        pdf_buffer = BytesIO()

        # Output the PDF to the BytesIO buffer
        pdf.output(pdf_buffer)

        # Seek to the beginning of the buffer
        pdf_buffer.seek(0)

        # Create a response
        response = FileResponse(pdf_buffer)
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment; filename="admission_letter.pdf"'
        return response