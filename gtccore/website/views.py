from django.http import FileResponse
from django.shortcuts import render
from django.views import View
from django.db.models import Q
from io import BytesIO
from dashboard.models import Application, Comment, Course, CourseCategory, Faq

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
        faqs = Faq.objects.all()
        context = {
            'faqs': faqs
        }
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
        application_id = request.GET.get('application_id')
        email = request.GET.get('email')
        phone = request.GET.get('phone')

        application = Application.objects.filter(
            Q(application_id=application_id) &
            Q(email=email) &
            Q(phone=phone)
        ).first()

        context = {
            'application': application
        }
        return render(request, self.template, context)


class CoursesView(View):
    '''Courses page view.'''
    template = 'website/courses.html'

    def get(self, request):
        category_name = request.GET.get('category_name') or None
        category_id = request.GET.get('category_id') or None
        category = None

        # recently added courses: 5
        latst_courses = Course.objects.all().order_by('-id')[:5]
        # set all courses as default
        courses = Course.objects.all()
        if category_id:
            category_id = int(category_id)
            category = CourseCategory.objects.filter(id=category_id).first()

        if category:
            courses = Course.objects.filter(category=category)

        categories = CourseCategory.objects.all()
        context = {
            'category_name': category_name,
            'category': category,
            'courses': courses,
            'categories': categories,
            'latst_courses': latst_courses
        }
        return render(request, self.template, context)


class CourseDetailsView(View):
    '''Course Details page view.'''
    template = 'website/course-details.html'

    def get(self, request):
        course_id = request.GET.get('course_id')
        course_id = int(course_id)
        course = Course.objects.filter(id=course_id).first()
        comments = Comment.objects.filter(course=course)
        categories = CourseCategory.objects.all()
        context = {
            'course': course,
            'comments': comments,
            'categories': categories
        }
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