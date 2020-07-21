from django import forms
from django.forms import ModelForm
from .models import Provider, Location



class ProviderForm(ModelForm):

    class Meta:
        model = Provider
        fields = ['name_first', 'name_last', 'abbrev', 'num_work_days']


class LocationForm(ModelForm):

    class Meta:
        model = Location
        fields = ['name', 'abbrev', 'provider_range', 'weekend']