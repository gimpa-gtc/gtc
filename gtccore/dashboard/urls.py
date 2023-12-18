from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('settings/preference', views.PreferenceSettingsView.as_view(), name='prefered_settings'), #noqa
    path('settings/password-reset', views.PasswordResetView.as_view(), name='password_reset'), #noqa
    path('settings/change-profile-pic', views.ChangeProfilePicView.as_view(), name='change_profile_pic'), #noqa
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
    path('download-notifications/', views.DownloadNotificationView.as_view(), name='download_notifications'), #noqa

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
# urlpatterns += [
#     path('facilitators/', views.FacilitorsView.as_view(), name='facilitators'),
#     path('download-facilitators/', views.DownloadFacilitatorsView.as_view(), name='download_facilitators'), #noqa
#     path('create-update-facilitator/', views.CreateUpdateFacilitatorView.as_view(), name='create_update_facilitator'), #noqa
# ]

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
    path('download-course-requests/', views.DownloadCourseRequestsView.as_view(), name='download_course_requests'), #noqa
    path('course-requests/', views.CourseRequestsView.as_view(), name='course_requests'), #noqa
    path('course-requests/reply/', views.ReplyCourseRequestView.as_view(), name='reply_course_request'), #noqa
    path('notifications/', views.NotificationsView.as_view(), name='notifications'), #noqa
    path('create-update-notification/', views.CreateUpdateNotificationView.as_view(), name='create_update_notification'), #noqa
    path('broadcast-notification/', views.BroadcastNotificationView.as_view(), name='broadcast'), #noqa
]

#Content Management
urlpatterns += [
    path('faqs/', views.FAQsView.as_view(), name='faqs'), #noqa
    path('create-update-faq/', views.CreateUpdateFAQView.as_view(), name='create_update_faq'), #noqa
    path('testimonials/', views.TestimonialsView.as_view(), name='testimonials'), #noqa
    path('create-update-testimonial/', views.CreateUpdateTestimonialView.as_view(), name='create_update_testimonial'), #noqa
    path('delete-faq/', views.DeleteFAQView.as_view(), name='delete_faq'), #noqa
    path('delete-testimonial/', views.DeleteTestimonialView.as_view(), name='delete_testimonial'), #noqa
    path('teams/', views.TeamsView.as_view(), name='teams'), #noqa
    path('create-update-team/', views.CreateUpdateTeamView.as_view(), name='create_update_team'), #noqa
    path('delete-team/', views.DeleteTeamView.as_view(), name='delete_team'), #noqa
    path('download-teams/', views.DownloadTeamsView.as_view(), name='download_teams'), #noqa
]

# gallery
urlpatterns += [
    path('image-categories/', views.ImageCategoriesView.as_view(), name='img_category'), #noqa
    path('create-update-img-cat/', views.CreateUpdateImageCategoryView.as_view(), name='create_update_img_cat'), #noqa
    path('images/', views.ImagesView.as_view(), name='images'), #noqa
    path('add-images/', views.AddImages.as_view(), name='add_images'), #noqa
    path('delete-image/', views.DeleteImageView.as_view(), name='delete_image'), #noqa
    path('delete-image-category/', views.DeleteImageCategoryView.as_view(), name='delete_img_cat'), #noqa
]