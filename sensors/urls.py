from django.urls import include, path

from sensors.views import index

urlpatterns = [
    path('', index, name='index'),
]