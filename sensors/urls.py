from django.urls import include, path

from sensors.views import index, lk, lk2

urlpatterns = [
    path('', index, name='index'),
    path('lk/', lk, name='lk'),
    # path('lk2/<int:pk>', lk, name='lk2'),
    path('lk2/<int:pk>', lk2, name='lk2'),

]
