from django.http import FileResponse
from django.shortcuts import redirect, render
from django.views import View
from django.db.models import Q
from io import BytesIO
from dashboard.forms import ApplicationForm
from dashboard.models import Application, Comment, Course, CourseCategory, Facilitator, Faq

from gtccore.library.services import generate_admission_letter
from django.http import HttpResponseRedirect


class HomeView(View):
    '''Home page view.'''
    template = 'website/index.html'

    def get(self, request):
        facilitators = Facilitator.objects.all()
        context = {
            'facilitators': facilitators
        }
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



class MakePaymentView(View):
    '''Make Payment page view.'''
    template = 'website/online-payment.html'

    def get(self, request):
        application_id = request.GET.get('application_id')
        application = Application.objects.filter(application_id=application_id).first() # noqa
        context = {
            'application': application
        }
        return render(request, self.template, context)
    
    def post(self, request):
        # implement payment logic here
        # implement payment logic here
        return redirect('website:enroll_success')

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



class EnrollView(View):
    '''Enroll page view.'''
    template = 'website/enroll.html'
    template_make_payment = 'website/online-payment.html'

    def get(self, request):
        course_id = request.GET.get('course_id')
        course_id = int(course_id)
        course = Course.objects.filter(id=course_id).first()
        context = {
            'course': course
        }
        return render(request, self.template, context)
    
    def post(self, request):
        form = ApplicationForm(request.POST)
        course_id = request.POST.get('course_id')
        pay_now = request.POST.get('pay_now')
        course_id = int(course_id)
        course = Course.objects.filter(id=course_id).first()
        if course is None:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if form.is_valid():
            application = form.save(commit=False)
            application.course = course                
            application.save()
            context = {
                'application': application
            }
            if pay_now:
                # redirect to payment page
                return render(request, self.template_make_payment, context)
            return redirect('website:enroll_success')
        
        context = {
            'course': course
        }
        return render(request, self.template, context)


class EnrollSuccessView(View):
    '''Enroll Success page view.'''
    template = 'website/enroll-success.html'

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