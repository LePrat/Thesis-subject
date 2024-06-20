from django.db import models


class Fund(models.Model):
    name = models.CharField(max_length=200)
    funder = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200)
    duration_in_months = models.PositiveIntegerField()
    min_years_since_phd = models.PositiveIntegerField()
    max_years_since_phd = models.PositiveIntegerField()
    link = models.URLField(max_length=200)
    fund_type = models.CharField(max_length=10, choices=[("fellowship", "Fellowship"), ("grant", "Grant")])

    def __str__(self):
        return self.name
