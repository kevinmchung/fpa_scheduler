from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect # noqa: 401
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic, View
from django.views.generic.edit import UpdateView

from .models import Provider, Location, ProviderVacation, ProviderLocationMax
from .forms import ProviderForm, LocationForm, ProviderLocationMaxForm, ProviderVacationFormSet, SchedulerForm
from django.forms import modelformset_factory, inlineformset_factory
from django.urls import reverse_lazy


class IndexView(generic.ListView):
    template_name = 'scheduler/index.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name)


# APP FUNCTIONS






# PROVIDER VIEWS

# TODO: Ensure unique abbrev fields and provide error/validation method

def new_provider_create_related_ProviderLocationMax(provider):

    location_list = Location.objects.all()

    for location in location_list:
        new = ProviderLocationMax(provider=provider, location=location)
        new.save()


class ProviderIndexView(generic.ListView):

    template_name = 'scheduler/provider_index.html'
    form_class = ProviderForm

    def get(self, request, **kwargs):
        return render(request, self.template_name, {'form': self.form_class, 'provider_list': Provider.objects.order_by('name_last')})


    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_provider = form.save()
            new_provider_create_related_ProviderLocationMax(new_provider)
            return HttpResponseRedirect(request.path_info)
        return render(request, self.template_name, {'form': form})


class ProviderDetailView(generic.DetailView):
    model = Provider
    template_name = 'scheduler/provider_detail.html'


class ProviderUpdateView(generic.UpdateView):
    model = Provider
    form_class = type('ProviderUpdateForm', (ProviderForm,), {'button_text': 'Update'})
    template_name = 'scheduler/provider_update.html'
    success_url = reverse_lazy('scheduler:provider-index')


class ProviderDeleteView(generic.DeleteView):
    model = Provider
    template_name = 'scheduler/provider_delete.html'
    success_url = reverse_lazy('scheduler:provider-index')




# LOCATION VIEWS

# TODO: Ensure unique abbrev fields and provide error/validation method

def new_location_create_related_ProviderLocationMax(location):

    provider_list = Provider.objects.all()

    for provider in provider_list:
        new = ProviderLocationMax(provider=provider, location=location)
        new.save()


class LocationIndexView(generic.ListView):

    template_name = 'scheduler/location_index.html'
    form_class = LocationForm

    def get(self, request, **kwargs):
        return render(request, self.template_name, {'form': self.form_class, 'location_list': Location.objects.order_by('name')})


    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_location = form.save()
            new_location_create_related_ProviderLocationMax(new_location)
            return HttpResponseRedirect(request.path_info)
        return render(request, self.template_name, {'form': form})




class LocationDetailView(generic.DetailView):
    model = Location
    template_name = 'scheduler/location_detail.html'


class LocationUpdateView(generic.UpdateView):
    model = Location
    form_class = type('LocationUpdateForm', (LocationForm,), {'button_text': 'Update'})
    template_name = 'scheduler/location_update.html'
    success_url = reverse_lazy('scheduler:location-index')


class LocationDeleteView(generic.DeleteView):
    model = Location
    template_name = 'scheduler/location_delete.html'
    success_url = reverse_lazy('scheduler:location-index')



# PREFERENCE VIEWS

# TODO: accommodate for no vacation days in index view (blank row means no bottom ing TD, so underline under edit button is missing)


class PreferenceIndexView(generic.ListView):

    template_name = 'scheduler/preference_index.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name,{
                      'provider_list': Provider.objects.order_by('name_last'),
                      'provider_location_max_list': ProviderLocationMax.objects.all(),
                      'provider_vacation_list': ProviderVacation.objects.all(),
                    })


class PreferenceDetailView(View):

    template_name = 'scheduler/preference_detail.html'

    def get(self, request, **kwargs):

        pk = self.kwargs['pk']
        provider = Provider.objects.get(id=pk)
        provider_location_max_list = ProviderLocationMax.objects.filter(provider_id=pk).order_by('location')
        provider_vacation_list = ProviderVacation.objects.filter(provider_id=pk).order_by('start_date')

        return render(request, self.template_name,{
                      'provider': provider,
                      'provider_location_max_list': provider_location_max_list,
                      'provider_vacation_list': provider_vacation_list,
                   })




# PROVIDER LOCATION MAX VIEWS

class ProviderLocationMaxUpdateView(View):

    # model = ProviderLocationMax
    # form_class = ProviderLocationMaxForm
    template_name = 'scheduler/preference_plm_update.html'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        provider = Provider.objects.get(pk=pk)
        plmFormset = inlineformset_factory(Provider, ProviderLocationMax, form=ProviderLocationMaxForm,
                                           fields=('provider_at_location_max_days',),
                                           can_delete=False, can_order=False, extra=0)
        formset = plmFormset(instance=provider)

        #formset = ProviderLocationMaxForm(provider)
        #plmFormset = modelformset_factory(ProviderLocationMax, fields=('location', 'provider_at_location_max_days',))
        #formset = plmFormset(queryset=ProviderLocationMax.objects.filter(provider_id=pk))

        return render(request, self.template_name, {'formset':formset, 'provider':provider})

    def post(self, request, **kwargs):

        pk = self.kwargs['pk']
        provider = Provider.objects.get(pk=pk)
        plmFormset = inlineformset_factory(Provider, ProviderLocationMax, form=ProviderLocationMaxForm,
                                           fields=('location', 'provider_at_location_max_days',),
                                           can_delete=False, can_order=False, extra=0)
        formset = plmFormset(request.POST, instance=provider)

        #plmFormset = modelformset_factory(ProviderLocationMax, fields=('location', 'provider_at_location_max_days',))
        #formset = plmFormset(queryset=ProviderLocationMax.objects.filter(provider_id=pk))

        if formset.is_valid():
            formset.save()
            #instances = formset.save(commit=False)
            #for i in instances:
            #    i.provider_id = pk
            #    i.save()

        return redirect('scheduler:preference-detail', pk=pk)



# PROVIDER VACATION VIEWS

# TODO: prevent duplicate dates for a provider
# TODO: date range picker

class ProviderVacationUpdateView(View):

    template_name = 'scheduler/preference_vacation_update.html'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        provider = Provider.objects.get(pk=pk)
        formset = ProviderVacationFormSet(instance=provider)

        return render(request, self.template_name, {'formset': formset, 'provider': provider})

    def post(self, request, **kwargs):

        pk = self.kwargs['pk']
        provider = Provider.objects.get(pk=pk)
        formset = ProviderVacationFormSet(request.POST, instance=provider)

        if formset.is_valid():
            formset.save()
            return redirect('scheduler:preference-detail', pk=pk)
        else:
            return render(request, self.template_name, {'formset': formset, 'provider': provider})


# MAKE SCHEDULE VIEWS

# TODO: Incorporate the scheduler logid

def make_schedule(start_date, end_date):

    locations = Location.objects.order_by('name')
    providers = Provider.objects.order_by('name_last')
    plms = ProviderLocationMax.objects.all()
    vacations = ProviderVacation.objects.order_by('vacation_date')

    ## ALL OF THE SCHEDULER LOGIC HAPPENS IN HERE

    schedule = 'hello'

    return schedule


class MakeScheduleIndexView(View):

    template_name = 'scheduler/makeschedule_index.html'
    form_class = SchedulerForm

    def get(self, request, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = SchedulerForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            schedule = make_schedule(cleaned_data['start_date'], cleaned_data['end_date'])
            return render(request, self.template_name, {'schedule': schedule})
        else:
            return render(request, self.template_name, {'form': self.form_class})

