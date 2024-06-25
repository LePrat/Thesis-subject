"""
URL mapping for the funds app.
"""
from django.urls import path
from .views import FundListView

urlpatterns = [
    path('', FundListView.as_view(), name='fund_list'),
]