from django.shortcuts import render


class CustomErrorMiddleware:
    '''
        Custom Error Middleware to handle 404 and 500 errors.
        Even when [DEBUG] is set to [True], this middleware will still render the custom error pages.
    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            return render(request, 'dashboard/404.html', status=404)
        
        elif response.status_code == 500:
            return render(request, 'dashboard/500.html', status=500)

        return response