from django.urls import path
from .scripts.dash1 import *

urlpatterns = [
    path('dash1_inclusion_q11/', dash1_inclusion_q11, name='dash1_inclusion_q11'),
    path('dash1_inclusion_q12/', dash1_inclusion_q12, name='dash1_inclusion_q12'),
]