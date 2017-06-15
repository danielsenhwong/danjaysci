from django.conf.urls import include, url

from . import views
from .views import InstitutionDetailView

urlpatterns = [
    url(r'^$',
        views.index,
        name = 'index'),
    url(r'^(?P<pk>[0-9]+)/$',
        InstitutionDetailView.as_view(),
        name='institution-detail'),
]
