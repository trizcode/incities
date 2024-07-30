from django.urls import path
from .scripts.dash1 import *
from .scripts.dash2 import *

urlpatterns = [
    # Inclusion
    path('dash1_inclusion_q11/', dash1_inclusion_q11, name='dash1_inclusion_q11'),
    path('dash1_inclusion_q12/', dash1_inclusion_q12, name='dash1_inclusion_q12'),
    # Sustainability
    path('dash2_q11/', dash2_q11, name='dash2_q11'), # Air quality
    path('dash2_q12/', dash2_q12, name='dash2_q12'),
    path('dash2_q21/', dash2_q21, name='dash2_q21'), # Clean city
    #path('dash2_q21/', dash2_q21, name='dash2_q21'), # Energy
]