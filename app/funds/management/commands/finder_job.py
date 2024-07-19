from django.core.management.base import BaseCommand
from funds.models import Fund
from needle.location_finder import run_finder


class Command(BaseCommand):
    def handle(self, *args, **options):
        funds = Fund.objects.filter(location_found=False).order_by('-id')[:14]
        run_finder(funds)
        self.stdout.write(self.style.SUCCESS('Locations found!'))
