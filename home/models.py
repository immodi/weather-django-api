from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, primary_key=True, db_index=True)
    country_name = models.CharField(max_length=80)
    lat = models.CharField(max_length=50)
    lng = models.CharField(max_length=50)
    iso = models.CharField(max_length=3)

    def __str__(self):
        return self.name