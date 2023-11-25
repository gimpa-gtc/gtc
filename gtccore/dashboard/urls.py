from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('invoices/', views.InvoiceListView.as_view(), name='invoices'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
]
