from django.shortcuts import render
from .models import Fund


def index(request):
    """render the funds page"""
    return render(request, 'funds/index.html',  {'funds': Fund.objects.all()})
