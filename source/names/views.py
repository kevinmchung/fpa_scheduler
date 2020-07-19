from django.shortcuts import render
from django.views import generic
from django.http import HttpResponseRedirect
from .models import Name
from .forms import NameForm

'''
class IndexView(generic.ListView):
    template_name = 'names/index.html'
    context_object_name = 'names_list'

    def get_queryset(self):
        return Name.objects.order_by('name_last')
'''

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


class EditView(generic.ListView):
    template_name = 'names/edit.html'
    context_object_name = 'names_list'

    def get_queryset(self):
        return Name.objects.order_by('name_last')


def name_delete(request):

    return render(request, 'names/index.html', {'form': form, 'names_list': Name.objects.order_by('name_last')})