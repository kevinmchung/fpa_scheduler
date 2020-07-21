from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from .models import Name
from .forms import NameForm
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView



class NameIndexView(generic.ListView):
    template_name = 'names/index.html'
    context_object_name = 'names_list'
    form_class = NameForm

    def get(self, request):
        #form_class = NameForm
        return render(request, 'names/index.html', {'form': self.form_class, 'names_list': Name.objects.order_by('name_last')})


    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)
        return render(request, self.template_name, {'form': form})



class NameDetailView(generic.DetailView):
    model = Name
    template_name = 'names/detail.html'


class NameUpdateView(generic.UpdateView):
    model = Name
    fields = ['name_first', 'name_last', 'abbr']
    template_name = 'names/update.html'


class NameDeleteView(generic.DeleteView):
    model = Name
    template_name = 'names/delete.html'
    success_url = reverse_lazy('names:index')


'''
class ResultsView(generic.DetailView):
    model = Names
    template_name = 'names/results.html'



def name_add(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            # redirect to a new URL:
            return HttpResponseRedirect(request.path_info)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'names/index.html', {'form': form, 'names_list': Name.objects.order_by('name_last')})

'''
'''
class EditView(generic.ListView):
    template_name = 'names/edit.html'
    context_object_name = 'names_list'

    def get_queryset(self):
        return Name.objects.order_by('name_last')

class EditView(generic.DetailView):
    model = Name
    template_name = 'names/edit.html'

'''


'''

def name_edit(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            # redirect to a new URL:
            return HttpResponseRedirect(request.path_info)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'names/index.html', {'form': form, 'names_list': Name.objects.order_by('name_last')})


def name_delete(request):

    return render(request, 'names/index.html', {'form': form, 'names_list': Name.objects.order_by('name_last')})

'''