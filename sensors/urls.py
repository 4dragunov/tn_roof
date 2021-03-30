from django.urls import include, path

from sensors.views import index, lk, lk2

urlpatterns = [
    path('', index, name='index'),
    path('lk/', lk, name='lk'),
    path('lk2/', lk2, name='lk2'),
]
