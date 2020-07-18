from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Name


class IndexView(generic.ListView):
    template_name = 'scheduler/index.html'

    def get_queryset(self):
        return 0



class NamesView(generic.ListView):
    template_name = 'scheduler/names.html'
    context_object_name = 'names_list'

    def get_queryset(self):
        return Name.objects.order_by('name_last')


