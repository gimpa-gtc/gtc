from django.shortcuts import render

def handler404(request, exception):
    template = 'error/404.html'
    return render(request, '404.html', status=404)


def handler500(request):
    template = 'error/404.html'
    return render(request, 'error/404.html', status=500)