from django.urls import include, path
from .views import DataSend, DataGet

v1_patterns = (
    [
       path('send/', DataSend.as_view()),
       path('get/', DataGet.as_view()),



    ]
)


urlpatterns = [
    path('v1/', include(v1_patterns)),
]