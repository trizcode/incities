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
    path('dash2_q11/', dash2_q11, name='dash2_q11'),
    path('dash2_q12/', dash2_q12, name='dash2_q12'), # Air quality
    path('dash2_q22/', dash2_q22, name='dash2_q22'), # Energy
    path('dash2_bar_chart_energy_ranking/', dash2_bar_chart_energy_ranking, name='dash2_bar_chart_energy_ranking'),
    path('d2_donut_chart_energy/', d2_donut_chart_energy, name='d2_donut_chart_energy'),
    
    path('d2_bar_chart_TPA_prot_area/', d2_bar_chart_TPA_prot_area, name='d2_bar_chart_TPA_prot_area'), # Biodiversity
    path('d2_bar_chart_MPA_prot_area/', d2_bar_chart_MPA_prot_area, name='d2_bar_chart_MPA_prot_area'),
    path('d2_donut_chart_prot_area/', d2_donut_chart_prot_area, name='d2_donut_chart_prot_area'),

    
    path('dash2_q41/', dash2_q41, name='dash2_q41'),
    path('dash2_line_chart_wst_oper/', dash2_line_chart_wst_oper, name='dash2_line_chart_wst_oper'), # Waste Management
    
    path('dash2_bar_chart_wst_ranking/', dash2_bar_chart_wst_ranking, name='dash2_bar_chart_wst_ranking'),
    
    path('dash2_q51/', dash2_q51, name='dash2_q51'),
    path('dash2_q52/', dash2_q52, name='dash2_q52'),
    path('dash2_q61/', dash2_q61, name='dash2_q61'), # Employment
    path('dash2_bar_chart_employment_ranking/', dash2_bar_chart_employment_ranking, name='dash2_bar_chart_employment_ranking'),
    
    path('dash2_donut_chart_employment_by_sex/', dash2_donut_chart_employment_by_sex, name='dash2_donut_chart_employment_by_sex'),
    # Resilience
    path('dash3_chart_1_1_ranking/', dash3_chart_1_1_ranking, name='dash3_chart_1_1_ranking'),
    path('dash3_chart_1_2_ranking/', dash3_chart_1_2_ranking, name='dash3_chart_1_2_ranking'),
    path('dash3_chart_1/', dash3_chart_1, name='dash3_chart_1'),
    path('dash3_chart_2/', dash3_chart_2, name='dash3_chart_2'),
    path('dash3_chart_3/', dash3_chart_3, name='dash3_chart_3'),
    path('dash3_chart_4/', dash3_chart_4, name='dash3_chart_4'),
]