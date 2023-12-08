from dashboard.models import CourseCategory


def get_course_categories(request):
    return {'all_categories': CourseCategory.objects.all()}