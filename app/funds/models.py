from django.db import models


class Fund(models.Model):
    name = models.CharField(max_length=400)
    funder = models.CharField(max_length=400)
    location = models.CharField(max_length=200, blank=True, null=True)
    nationality = models.CharField(max_length=200,  blank=True, null=True)
    duration_in_months = models.PositiveIntegerField(blank=True,  null=True)
    min_years_since_phd = models.PositiveIntegerField(blank=True,  null=True)
    max_years_since_phd = models.PositiveIntegerField(blank=True,  null=True)
    max_fund_amount = models.CharField(max_length=200, blank=True, null=True)
    eligibility_text = models.TextField(blank=True,  null=True)
    link = models.URLField(max_length=400)

    def __str__(self):
        return self.name
