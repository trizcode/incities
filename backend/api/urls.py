from django.urls import path
from . import views

urlpatterns = [
    path('fetch_eurostat_data/', views.fetch_eurostat_data, name='fetch_eurostat_data'),
    path('fetch_openweather_data/', views.fetch_openweather_data, name='fetch_openweather_data'),
]