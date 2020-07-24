from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect # noqa: 401
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic, View

from .models import Provider, Location, ProviderVacation, ProviderLocationMax
from .forms import ProviderForm, LocationForm, ProviderLocationMaxForm
from django.forms import modelformset_factory, inlineformset_factory
from django.urls import reverse_lazy


class IndexView(generic.ListView):
    template_name = 'scheduler/index.html'

    def get_queryset(self):
        return 0


# APP FUNCTIONS






# PROVIDER VIEWS

def new_provider_create_related_ProviderLocationMax(provider):

    location_list = Location.objects.all()

    for location in location_list:
        new = ProviderLocationMax(provider=provider, location=location)
        new.save()


class ProviderIndexView(generic.ListView):

    template_name = 'scheduler/provider_index.html'
    form_class = ProviderForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class, 'provider_list': Provider.objects.order_by('name_last')})


    def post(self, request):
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
    form_class = ProviderForm
    template_name = 'scheduler/provider_update.html'
    success_url = reverse_lazy('scheduler:provider-index')


class ProviderDeleteView(generic.DeleteView):
    model = Provider
    template_name = 'scheduler/provider_delete.html'
    success_url = reverse_lazy('scheduler:provider-index')




# LOCATION VIEWS


def new_location_create_related_ProviderLocationMax(location):

    provider_list = Provider.objects.all()

    for provider in provider_list:
        new = ProviderLocationMax(provider=provider, location=location)
        new.save()


class LocationIndexView(generic.ListView):

    template_name = 'scheduler/location_index.html'
    form_class = LocationForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class, 'location_list': Location.objects.order_by('name')})


    def post(self, request):
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
    form_class = LocationForm
    template_name = 'scheduler/location_update.html'
    success_url = reverse_lazy('scheduler:location-index')


class LocationDeleteView(generic.DeleteView):
    model = Location
    template_name = 'scheduler/location_delete.html'
    success_url = reverse_lazy('scheduler:location-index')



# PREFERENCE VIEWS

class PreferenceIndexView(generic.ListView):

    template_name = 'scheduler/preference_index.html'

    def get(self, request):
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
        provider_vacation_list = ProviderVacation.objects.filter(provider_id=pk).order_by('vacation_date')

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

    def get(self, request,**kwargs):
        pk = self.kwargs['pk']
        provider = Provider.objects.get(pk=pk)
        plmFormset = inlineformset_factory(Provider, ProviderLocationMax,
                                           fields=('location','provider_at_location_max_days',),
                                           #inlines= [provider],
                                           can_delete=False, can_order=False, extra=0)
        formset = plmFormset(instance=provider)

        #formset = ProviderLocationMaxForm(provider)
        #plmFormset = modelformset_factory(ProviderLocationMax, fields=('location', 'provider_at_location_max_days',))
        #formset = plmFormset(queryset=ProviderLocationMax.objects.filter(provider_id=pk))

        return render(request, self.template_name, {'formset':formset, 'provider':provider})

    def post(self, request, *args, **kwargs):

        pk = self.kwargs['pk']
        provider = Provider.objects.get(pk=pk)
        plmFormset = inlineformset_factory(Provider, ProviderLocationMax,
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

