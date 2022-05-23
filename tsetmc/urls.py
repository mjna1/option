from django.urls import path, include
from .views import home, api, api2, home1

urlpatterns = [
    path("w", home, name='home'),
    path("api", api, name='home'),
    path("api2", api2, name='home'),
    path("", home1, name='home'),

]
