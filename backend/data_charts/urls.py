from django.urls import path
from .scripts.dash1 import *
from .scripts.dash2 import *
from .scripts.dash3 import *
from .scripts.utils import *

urlpatterns = [
    path('get_available_years/', get_available_years, name ='get_available_years'),
    # Inclusion
    path('dash1_line_chart/', dash1_line_chart, name='dash1_line_chart'),
    path('dash1_bar_chart_ranking/', dash1_bar_chart_ranking, name='dash1_bar_chart_ranking'),
    path('dash1_gini_coef_vs_poverty_risk/', dash1_gini_coef_vs_poverty_risk, name='dash1_gini_coef_vs_poverty_risk'),
    path('disability_employment_gap_by_sex/', disability_employment_gap_by_sex, name='disability_employment_gap_by_sex'),
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
    # Resilience
    path('dash3_chart_1/', dash3_chart_1, name='dash3_chart_1'), # Social
    path('dash3_chart_2/', dash3_chart_2, name='dash3_chart_2'),
    path('dash3_chart_3/', dash3_chart_3, name='dash3_chart_3'), # Economic & Infrastructure
    path('dash3_chart_4/', dash3_chart_4, name='dash3_chart_4'), # Economic vs Infrastructure
]