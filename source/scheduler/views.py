from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'scheduler/index.html'

    def get_queryset(self):
        return 0

