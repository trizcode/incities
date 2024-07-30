from django.urls import path
from . import views

urlpatterns = [
    path('dash1_inclusion_q11/', views.dash1_inclusion_q11, name='dash1_inclusion_q11'),
    path('dash1_inclusion_q12/', views.dash1_inclusion_q12, name='dash1_inclusion_q12'),
]