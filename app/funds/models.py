from django.db import models


class Fund(models.Model):
    name = models.CharField(max_length=200)
    funder = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    nationality = models.CharField(max_length=200)
    duration_in_months = models.PositiveIntegerField(blank=True)
    min_years_since_phd = models.PositiveIntegerField(blank=True)
    max_years_since_phd = models.PositiveIntegerField(blank=True)
    max_fund_amount = models.CharField(max_length=200)
    link = models.URLField(max_length=200)

    def __str__(self):
        return self.name
