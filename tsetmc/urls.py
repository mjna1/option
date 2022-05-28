from django.urls import path, include
from .views import url, api, api2, home1

urlpatterns = [
    path("url/<str:stock>", url, name='url'),
    path("api", api, name='api'),
    path("api2", api2, name='api2'),
    path("", home1, name='home1'),

]
