from django import forms
from django.forms import ModelForm,inlineformset_factory
from .models import Provider, Location, ProviderVacation, ProviderLocationMax
from django.utils.translation import gettext_lazy as _


class ProviderForm(ModelForm):

    class Meta:
        model = Provider
        fields = '__all__'
        #fields = ['name_first', 'name_last', 'abbrev', 'days_per_week']

        labels = {
            'name_first': _('First Name'),
            'name_last': _('Last Name'),
            'abbr': _('Abbreviation'),
            'days_per_week': _('Working Days Per Week'),
        }
        help_texts = {
            'abbrev': _('(3 letters)'),
        }

    def clean_abbrev(self):
        return self.cleaned_data['abbrev'].upper()


class LocationForm(ModelForm):

    class Meta:
        model = Location
        fields = '__all__'
        #fields = ['name', 'abbrev', 'provider_min', 'provider_max', 'weekend']

        labels = {
            'provider_min': _('Min Number of Providers Needed'),
            'provider_max': _('Max Number of Providers Needed'),
            'weekend': _('Weekend Coverage Needed'),
        }

        help_texts = {
            'abbrev': _('(5 letters)'),
        }

    def clean_abbrev(self):
        return self.cleaned_data['abbrev'].upper()



class ProviderLocationMaxForm(Provider):
    # NOT USED RIGHT NOW
    plm_formset = inlineformset_factory(Provider, ProviderLocationMax,
                                       fields=('location', 'provider_at_location_max_days',),
                                       can_delete=False, can_order=False, extra=0)



