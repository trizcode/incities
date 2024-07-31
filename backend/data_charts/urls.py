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
    path('dash2_q22/', dash2_q22, name='dash2_q22'), # Energy
    path('dash2_q31/', dash2_q31, name='dash2_q31'),
    path('dash2_q32/', dash2_q32, name='dash2_q32'), # Biodiversity
    path('dash2_q41/', dash2_q41, name='dash2_q41'),
    path('dash2_q42/', dash2_q42, name='dash2_q42'), # Waste Management
    path('dash2_q51/', dash2_q51, name='dash2_q51'),
    path('dash2_q52/', dash2_q52, name='dash2_q52'),
    path('dash2_q61/', dash2_q61, name='dash2_q61'), # Employment
    path('dash2_q62/', dash2_q62, name='dash2_q62'),
]