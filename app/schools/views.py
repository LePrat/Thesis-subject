from django.shortcuts import render


def index(request):
    """render the schools page"""
    return render(request, 'schools/index.html')
