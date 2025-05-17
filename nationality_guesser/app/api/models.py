from django.db import models
from django.utils import timezone


class Country(models.Model):
    country_code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    subregion = models.CharField(max_length=100, blank=True, null=True)
    is_independent = models.BooleanField(default=True)

    google_maps_link = models.URLField(blank=True, null=True)
    openstreetmap_link = models.URLField(blank=True, null=True)

    capital = models.CharField(max_length=100, blank=True, null=True)
    capital_latitude = models.FloatField(blank=True, null=True)
    capital_longitude = models.FloatField(blank=True, null=True)

    flag_png = models.URLField(blank=True, null=True)
    flag_svg = models.URLField(blank=True, null=True)
    flag_alt = models.TextField(blank=True, null=True)

    coat_of_arms_org = models.URLField(blank=True, null=True)
    coat_of_arms_png = models.URLField(blank=True, null=True)

    border = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.country_code})"


class NameNationality(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE)
    probability = models.FloatField()
    count = models.PositiveIntegerField(default=1)
    last_accessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "country")
        ordering = ["-probability"]

    def __str__(self):
        return f"{self.name} -> {self.country} ({self.probability:.2f})"
