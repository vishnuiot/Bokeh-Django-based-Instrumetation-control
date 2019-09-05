# /Django_instrument_project/urls.py
from django.conf.urls import url
from . import views
 
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^scan/$', views.scan, name='scan'),
    url(r'^stopscan/$', views.stopscan, name='stopscan'),
    url(r'^getmeasurement/$', views.getmeasurement, name='getmeasurement'),
    url(r'^startmeasurement/$', views.startmeasurement, name='startmeasurement'),
    url(r'^stopmeasurement/$', views.stopmeasurement, name='stopmeasurement'),
    url(r'^calibrate/$', views.Calibrate, name='Calibrate'),
    url(r'^reset/$', views.reset, name='reset')
]


