from django.urls import include, path
from .views import DataSend

v1_patterns = (
    [
       path('send/', DataSend.as_view())

    ]
)


urlpatterns = [
    path('v1/', include(v1_patterns)),
]