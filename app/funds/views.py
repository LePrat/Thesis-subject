from django.views.generic import ListView
from .models import Fund


class FundListView(ListView):
    model = Fund
    template_name = 'funds/index.html'
    context_object_name = 'funds'
    ordering = ['-id']
