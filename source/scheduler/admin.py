# Register your models here.

from django.contrib import admin

from .models import Provider, Location, ProviderVacation, ProviderLocationMax


admin.site.register(Provider)
admin.site.register(Location)
admin.site.register(ProviderVacation)
admin.site.register(ProviderLocationMax)