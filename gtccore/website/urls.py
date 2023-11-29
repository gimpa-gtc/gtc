from django.urls import path

from . import views

app_name = 'website'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faqs/', views.FaqsView.as_view(), name='faqs'),
]

# applications
urlpatterns += [
    path('application/', views.ApplicationView.as_view(), name='application'),
    path('application/status/', views.ApplicationStatusView.as_view(), name='application_status'), #noqa
    path('application/download/', views.DownloadAdmissionLetterView.as_view(), name='download_letter'), #noqa
]

# courses
urlpatterns += [
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('courses-details/', views.CourseDetailsView.as_view(), name='course_details'), #noqa
    path('enroll/', views.EnrollView.as_view(), name='enroll'),
    path('enroll/success', views.EnrollSuccessView.as_view(), name='enroll_success'),
]

# payment
urlpatterns += [
    path('make-payment/', views.MakePaymentView.as_view(), name='make_payment'),
]