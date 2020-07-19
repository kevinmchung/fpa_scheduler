from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Name
from .forms import NameForm

class IndexView(generic.ListView):
    template_name = 'scheduler/index.html'

    def get_queryset(self):
        return 0


class NamesView(generic.ListView):
    template_name = 'scheduler/names.html'
    context_object_name = 'names_list'

    def get_queryset(self):
        return Name.objects.order_by('name_last')



def name_add(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            print(form.cleaned_data)
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'scheduler/names.html', {'form': form, 'names_list': Name.objects.order_by('name_last')})
