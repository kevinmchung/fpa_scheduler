from django.urls import path

from . import views

app_name = 'scheduler'



urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # names has been moved to names app -- not needed here anymore
    #path('names/', views.name_add, name='names'),
    #path('names/<int:pk>/', views.NamesView.as_view(), name='namesdetail'),
]
