from django.urls import path
from . import views

app_name = 'names'

# URLs will resolve on first match

urlpatterns = [

    path('', views.NameIndexView.as_view(), name='index'),
    path('<int:pk>/update', views.NameUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.NameDeleteView.as_view(), name='delete'),
    path('<int:pk>', views.NameDetailView.as_view(), name='detail'),

]
