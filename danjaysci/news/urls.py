from django.conf.urls import url

from . import views

app_name = 'news'
urlpatterns = [
    # ex: /news/
    url(r'^$',
        views.index,
        name = 'index'),
    # ex: /news/5/
    url(r'^(?P<post_id>[0-9]+)/$',
        views.detail,
        name = 'detail'),
]
