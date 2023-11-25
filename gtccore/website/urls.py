from django.urls import path
from . import views

app_name = 'website'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faqs/', views.FaqsView.as_view(), name='faqs'),
]
