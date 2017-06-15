from django.conf.urls import include, url

from . import views
from .views import SupplyListView, SupplyDetailView, OrderListView, OrderDetailView

app_name = "supplies"
urlpatterns = [
    #url(r'^$', views.index, name = 'index'),
    url(r'^$',
        SupplyListView.as_view(),
        name='supply-list'),
    url(r'^(?P<pk>[0-9]+)/$',
        SupplyDetailView.as_view(),
        name='supply-detail'),
    url(r'^order/$',
        OrderListView.as_view(),
        name='order-list'),
    url(r'^order/(?P<pk>[0-9]+)/$',
        OrderDetailView.as_view(),
        name='order-detail'),
]
