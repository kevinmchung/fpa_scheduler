# Register your models here.

from django.contrib import admin

from .models import Provider, Office

admin.site.register(Provider)
admin.site.register(Office)