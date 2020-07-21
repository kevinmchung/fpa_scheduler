# Register your models here.

from django.contrib import admin

from .models import Provider, Location

#admin.site.register(Preference)
admin.site.register(Provider)
admin.site.register(Location)