from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
]

# users
urlpatterns += [
    path('users/', views.UsersView.as_view(), name='users'),
    path('create-update-user/', views.CreateUpdateUser.as_view(), name='create_update_user'), #noqa
    path('update-user-pic/', views.UpdateUserProfilePicView.as_view(), name='update_profile_pic'), #noqa
    path('download-users/', views.DownloadUsersView.as_view(), name='download_users'), #noqa
]


# applications
urlpatterns += [
    path('applications/', views.ApplicationsView.as_view(), name='applications'),
    path('create-update-application/', views.CreateUpdateApplicationView.as_view(), name='create_update_application'), #noqa
    path('admissions/', views.AdmissionsView.as_view(), name='admissions'),
    path('give-admission/', views.GiveAdmissionView.as_view(), name='give_admission'), #noqa
    path('applicants/', views.ApplicantsView.as_view(), name='applicants'),
]


# downloads
urlpatterns += [
    path('download-applications/', views.DownloadApplicationsView.as_view(), name='download_applications'), #noqa
    path('download-applicants/', views.DownloadApplicantsView.as_view(), name='download_applicants'), #noqa
    path('download-admissions/', views.DownloadAdmissionsView.as_view(), name='download_admissions'), #noqa
    path('download-cohorts/', views.DownloadCohortView.as_view(), name='download_cohorts'), #noqa
    path('download-courses/', views.DownloadCoursesView.as_view(), name='download_courses'), #noqa
    path('download-categories/', views.DownloadCategoriesView.as_view(), name='download_categories'), #noqa
]

# courses
urlpatterns += [
    path('courses/', views.CoursesView.as_view(), name='courses'),
    path('create-update-course/', views.CreateUpdateCourseView.as_view(), name='create_update_course'), #noqa
    path('create-update-category/', views.CreateUpdateCourseCategoryView.as_view(), name='create_update_category'), #noqa
    path('course-categories/', views.CourseCategoriesView.as_view(), name='course_categories'), #noqa
    path('cohorts/', views.CohortsView.as_view(), name='cohorts'), #noqa
    path('create-update-cohort/', views.CreateUpdateCohortView.as_view(), name='create_update_cohort'), #noqa
]

# facilitators
urlpatterns += [
    path('facilitators/', views.FacilitorsView.as_view(), name='facilitators'),
    path('download-facilitators/', views.DownloadFacilitatorsView.as_view(), name='download_facilitators'), #noqa
    path('create-update-facilitator/', views.CreateUpdateFacilitatorView.as_view(), name='create_update_facilitator'), #noqa
]

# payments
urlpatterns += [
    path('payments/', views.PaymentsView.as_view(), name='payments'),
    path('create-payment/', views.CreatePaymentView.as_view(), name='create_payment'), #noqa
    path('download-payments/', views.DownloadPaymentsView.as_view(), name='download_payments'), #noqa
]

#Support
urlpatterns += [
    path('contact-messages/', views.ContactMessagesView.as_view(), name='contact_messages'), #noqa
    path('contact-messages/reply/', views.ReplyMessageView.as_view(), name='reply_message'), #noqa
    path('download-contact-messages/', views.DownloadContactMessagesView.as_view(), name='download_contact_messages'), #noqa
    path('course-requests/', views.CourseRequestsView.as_view(), name='course_requests'), #noqa
    path('course-requests/reply/', views.ReplyCourseRequestView.as_view(), name='reply_course_request'), #noqa
    path('download-course-requests/', views.DownloadCourseRequestsView.as_view(), name='download_course_requests'), #noqa
    path('notifications/', views.NotificationsView.as_view(), name='notifications'), #noqa
    path('create-update-notification/', views.CreateUpdateNotificationView.as_view(), name='create_update_notification'), #noqa
]