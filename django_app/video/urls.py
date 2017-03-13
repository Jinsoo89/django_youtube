from django.conf.urls import url

from video import views

app_name = 'video'
urlpatterns = [
    url(r'^search/$', views.search_results, name='search'),
    url(r'^bookmark/$', views.bookmark_list, name='bookmark_list'),
    url(r'^bookmark/add/$', views.bookmark_toggle, name='bookmark_toggle'),
]
