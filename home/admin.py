from django.contrib import admin
from home.models import City

class Admin(admin.ModelAdmin):
    list_display = ['name', 'country_name', 'lat', 'lng', 'iso'] 


admin.site.register(City, Admin)