"""
URL mapping for the schools app.
"""
from django.urls import path
from schools import views

urlpatterns = [
    path('', views.index, name='index')
]
