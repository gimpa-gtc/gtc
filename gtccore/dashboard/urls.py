from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
]

# users
urlpatterns += [
    path('users/', views.UsersView.as_view(), name='users'),
    path('create-update-user/', views.CreateUpdateUser.as_view(), name='create_update_user'), #noqa
    path('download-users/', views.DownloadUsersView.as_view(), name='download_users'), #noqa
]


# applications
urlpatterns += [
    path('applications/', views.ApplicationsView.as_view(), name='applications'),
    path('admissions/', views.AdmissionsView.as_view(), name='admissions'),
    path('applicants/', views.ApplicantsView.as_view(), name='applicants'),
]

# courses
urlpatterns += [
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('course-categories/', views.CourseCategoriesView.as_view(), name='course_categories'), #noqa
]

# payments
urlpatterns += [
    path('payments/', views.PaymentsView.as_view(), name='payments'),
]