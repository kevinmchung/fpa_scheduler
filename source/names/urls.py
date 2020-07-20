from django.urls import path
from . import views

app_name = 'names'

urlpatterns = [

    path('', views.NameIndexView.as_view(), name='name-index'),
    #path('<int:pk>', views.NameDetailView.as_view(), name='name-detail'),
    #path('<int:pk>/update', views.NameUpdateView.as_view(), name='name-update'),

    # path('', views.IndexView.as_view(), name='index'),
    # path('', views.name_add, name='add'),
    # path('<int:pk>/edit', views.EditView.as_view(), name='edit'),

]
