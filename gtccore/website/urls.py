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