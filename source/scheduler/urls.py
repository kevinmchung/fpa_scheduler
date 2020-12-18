from django.urls import path

from . import views

app_name = 'scheduler'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('provider', views.ProviderIndexView.as_view(), name='provider-index'),
    path('provider/<int:pk>/update', views.ProviderUpdateView.as_view(), name='provider-update'),
    path('provider/<int:pk>/delete', views.ProviderDeleteView.as_view(), name='provider-delete'),
    path('provider/<int:pk>', views.ProviderDetailView.as_view(), name='provider-detail'),

    path('location', views.LocationIndexView.as_view(), name='location-index'),
    path('location/<int:pk>/update', views.LocationUpdateView.as_view(), name='location-update'),
    path('location/<int:pk>/delete', views.LocationDeleteView.as_view(), name='location-delete'),
    path('location/<int:pk>', views.LocationDetailView.as_view(), name='location-detail'),

    path('preference', views.PreferenceIndexView.as_view(), name='preference-index'),
    path('preference/<int:pk>', views.PreferenceDetailView.as_view(), name='preference-detail'),

    path('preference/plm/<int:pk>/update', views.ProviderLocationMaxUpdateView.as_view(), name='preference-plm-update'),
    path('preference/vacation/<int:pk>/update', views.ProviderVacationUpdateView.as_view(), name='preference-vacation-update'),

    path('makeschedule', views.MakeScheduleIndexView.as_view(), name='makeschedule-index'),

    path('download/<str:path>', views.download_schedule, name='download'),

]
