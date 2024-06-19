from django.db import models


class Fund(models.Model):
    name = models.CharField(max_length=200)
    funder = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    nationality = models.CharField(max_length=200)
    duration_in_months = models.PositiveIntegerField()
    years_since_phd_start = models.PositiveIntegerField()
    years_since_phd_end = models.PositiveIntegerField()
    link = models.URLField(max_length=200)
    fund_type = models.CharField(max_length=10, choices=[("fellowship", "Fellowship"), ("grant", "Grant")])

    def __str__(self):
        return self.name
