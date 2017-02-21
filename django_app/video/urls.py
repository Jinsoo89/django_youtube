from django.conf.urls import url

from video import views

app_name = 'video'
urlpatterns = [
    url(r'^search/$', views.save_to_db, name='search'),
    # url(r'^list/$', views.display_list, name='list'),

]