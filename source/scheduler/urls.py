from django.urls import path

from . import views

app_name = 'scheduler'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('names/', views.NamesView.as_view(), name='names'),
]
