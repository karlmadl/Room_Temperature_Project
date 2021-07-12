# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
from django.db import models


class TemperatureData(models.Model):
    inside_temperature = models.IntegerField(blank=True, null=True)
    outside_temperature = models.IntegerField(blank=True, null=True)
    season = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'temperature_data'


class Temperatures(models.Model):
    inside_temperature = models.IntegerField(blank=True, null=True)
    outside_temperature = models.IntegerField(blank=True, null=True)
    season = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'temperatures'
