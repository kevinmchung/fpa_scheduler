from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Provider, Location
from .forms import ProviderForm, LocationForm
from django.urls import reverse_lazy

class IndexView(generic.ListView):
    template_name = 'scheduler/index.html'

    def get_queryset(self):
        return 0



# PROVIDER VIEWS

class ProviderIndexView(generic.ListView):

    template_name = 'scheduler/provider_index.html'
    form_class = ProviderForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class, 'provider_list': Provider.objects.order_by('name_last')})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)
        return render(request, self.template_name, {'form': form})


class ProviderDetailView(generic.DetailView):
    model = Provider
    template_name = 'scheduler/provider_detail.html'


class ProviderUpdateView(generic.UpdateView):
    model = Provider
    fields = ['name_first', 'name_last', 'abbrev', 'num_work_days']
    template_name = 'scheduler/provider_update.html'
    success_url = reverse_lazy('scheduler:provider-index')


class ProviderDeleteView(generic.DeleteView):
    model = Provider
    template_name = 'scheduler/provider_delete.html'
    success_url = reverse_lazy('scheduler:provider-index')




# LOCATION VIEWS

class LocationIndexView(generic.ListView):

    template_name = 'scheduler/location_index.html'
    form_class = LocationForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class, 'location_list': Location.objects.order_by('name')})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)
        return render(request, self.template_name, {'form': form})


class LocationDetailView(generic.DetailView):
    model = Location
    template_name = 'scheduler/location_detail.html'


class LocationUpdateView(generic.UpdateView):
    model = Location
    fields = ['name', 'abbrev', 'provider_range', 'weekend']
    template_name = 'scheduler/location_update.html'
    success_url = reverse_lazy('scheduler:location-index')


class LocationDeleteView(generic.DeleteView):
    model = Location
    template_name = 'scheduler/location_delete.html'
    success_url = reverse_lazy('scheduler:location-index')