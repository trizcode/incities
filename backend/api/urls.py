from django.urls import path
from . import views

urlpatterns = [
    path('api/fetch_data/', views.fetch_data, name='fetch_data'),
]