from django.urls import include, path

from sensors.views import index, lk

urlpatterns = [
    path('', index, name='index'),
    path('lk/', lk, name='lk'),
]
