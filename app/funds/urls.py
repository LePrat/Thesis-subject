"""
URL mapping for the funds app.
"""
from django.urls import path
from funds import views

urlpatterns = [
    path('', views.index, name='index')
]
