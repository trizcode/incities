from django.urls import path
from . import views

urlpatterns = [
    path('dash1_inclusion_q11/', views.dash1_inclusion_q11, name='dash1_inclusion_q11'),
]