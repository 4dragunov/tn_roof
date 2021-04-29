from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from sensors.views import index, lk, lk2, dashboard, snow_settings, building_settings

urlpatterns = [
    # path('', index, name='index'),
    path('lk/', lk, name='lk'),
    # path('lk2/<int:pk>', lk, name='lk2'),
    path('lk2/<int:building_id>', lk2, name='lk2'),
    path('', dashboard, name='dashboard'),
    path('dashboard', dashboard, name='dashboard'),
    path('dashboard/snow_settings', snow_settings, name='snow_settings'),
    path('dashboard/building_settings', building_settings, name='building_settings'),

    path("auth/", include("users.urls")),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)