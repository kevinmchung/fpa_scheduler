from django import forms
from django.forms import Form, ModelForm, inlineformset_factory
from .models import Provider, Location, ProviderVacation, ProviderLocationMax
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div, Layout, Field
from bootstrap_datepicker_plus import DatePickerInput


class ProviderForm(ModelForm):
    button_text = 'Add'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.layout = Layout(
            Div(
                Div('name_first', css_class='col-sm-4'),
                Div('name_last', css_class='col-sm-4'),
                css_class='row',
            ),
            Div(
                Div('abbrev', css_class='col-sm-4'),
                css_class='row',
            ),
            Div(
                Div('days_per_week', css_class='col-sm-4'),
                css_class='row',
            ),
        )

        self.helper.add_input(Submit('submit', self.button_text))

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
            'abbrev': _('3 letters'),
        }

    def clean_abbrev(self):
        return self.cleaned_data['abbrev'].upper()

    def clean(self):
        cleaned_data = self.cleaned_data
        days_per_week = cleaned_data.get('days_per_week')
        if days_per_week > 5:
            self.add_error('days_per_week', _('Maximum number of working days per week is 5.'))

        return cleaned_data


class LocationForm(ModelForm):
    button_text = 'Add'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.layout = Layout(
            Div(
                Div('name', css_class='col-sm-6'),
                Div('abbrev', css_class='col-sm-2'),
                css_class='row',
            ),
            Div(
                Div('provider_min', css_class='col-sm-4'),
                Div('provider_max', css_class='col-sm-4'),
                css_class='row',
            ),
            Div(
                Div('weekend', css_class='col-sm-4'),
                css_class='row',
            ),
            Div(
                Div('num_providers_weekend', css_class='col-sm-4'),
                css_class='row',
            ),
        )

        self.helper.add_input(Submit('submit', self.button_text))

    class Meta:
        model = Location
        fields = '__all__'
        #fields = ['name', 'abbrev', 'provider_min', 'provider_max', 'weekend']

        labels = {
            'provider_min': _('Min Number of Providers Needed'),
            'provider_max': _('Max Number of Providers Needed'),
            'weekend': _('Weekend Coverage Needed'),
            'num_providers_weekend': _('Number of Providers on Weekends'),
        }

        help_texts = {
            'abbrev': _('5 letters'),
            'num_providers_weekend': _('Enter 0 if no weekend coverage needed')
        }

    def clean_abbrev(self):
        return self.cleaned_data['abbrev'].upper()

class ProviderVacationForm(ModelForm):

    class Meta:
        model = ProviderVacation
        fields = ('start_date', 'end_date')
        widgets = {
            'start_date': DatePickerInput(),
            'end_date': DatePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ProviderVacationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.helper.layout = Layout(
            Div(
                Div('start_date', css_class='col-sm-4'),
                Div('end_date', css_class='col-sm-4'),
                Field('DELETE', css_class='input_small'),
                css_class='row'
            ),
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', _('End date should not be before start date'))

        return cleaned_data


ProviderVacationFormSet = inlineformset_factory(Provider, ProviderVacation, form=ProviderVacationForm,
                                                fields=('start_date', 'end_date'), extra=0, can_delete=True)

class ProviderLocationMaxForm(ModelForm):

    class Meta:
        model = ProviderLocationMax
        fields = ('provider_at_location_max_days',)

    def __init__(self, *args, **kwargs):
        super(ProviderLocationMaxForm, self).__init__(*args, **kwargs)

        # print(args, kwargs)

        plm = kwargs.get('instance')

        self.fields['provider_at_location_max_days'].label = plm.location

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'


class SchedulerForm(Form):
    start_date = forms.DateField(widget=DatePickerInput())
    end_date = forms.DateField(widget=DatePickerInput())

    def __init__(self, *args, **kwargs):
        super(SchedulerForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Div(
                Div('start_date', css_class='col-sm-6'),
                Div('end_date', css_class='col-sm-6'),
                css_class='row',
            ),
        )

        self.helper.add_input(Submit('submit', 'Generate'))

