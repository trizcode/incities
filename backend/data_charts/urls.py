from django.urls import path
from .dashboards.inclusion import *
from .dashboards.sustainability import *
from .dashboards.resilience import *
from .scripts.utils import *

urlpatterns = [
    
    # Inclusion dashboard
    path('line_chart_inclusion/', line_chart_inclusion, name='line_chart_inclusion'),
    path('map_inclusion/', map_inclusion, name='map_inclusion'),
    path('bar_chart_inclusion/', bar_chart_inclusion, name='bar_chart_inclusion'),
    path('donut_chart_inclusion/', donut_chart_inclusion, name='donut_chart_inclusion'),
    
    # Sustainability dashboard
    
    # Air quality
    path('grouped_bar_chart_air_quality/', grouped_bar_chart_air_quality, name='grouped_bar_chart_air_quality'),
    path('bar_chart_air_quality/', bar_chart_air_quality, name="bar_chart_air_quality"),
    path('card_air_quality/', card_air_quality, name='card_air_quality'),
    path('line_chart_air_quality/', line_chart_air_quality, name='line_chart_air_quality'),
    
    # Energy
    path('line_chart_energy/', line_chart_energy, name='line_chart_energy'),
    path('bar_chart_energy/', bar_chart_energy, name='bar_chart_energy'),
    path('donut_chart_energy/', donut_chart_energy, name='donut_chart_energy'),
    
    # Biodiversity
    path('bar_chart_TPA_prot_area/', bar_chart_TPA_prot_area, name='bar_chart_TPA_prot_area'),
    path('bar_chart_MPA_prot_area/', bar_chart_MPA_prot_area, name='bar_chart_MPA_prot_area'),
    path('grouped_bar_chart_prot_area/', grouped_bar_chart_prot_area, name='grouped_bar_chart_prot_area'),
    path('donut_chart_prot_area/', donut_chart_prot_area, name='donut_chart_prot_area'),
    
    # Waste Management
    #path('line_chart_wst_oper/', line_chart_wst_oper, name='line_chart_wst_oper'),
    #path('bar_chart_wst_oper_ranking/', bar_chart_wst_oper_ranking, name='bar_chart_wst_oper_ranking'),
    #path('horizontal_bar_chart_waste_treat/', horizontal_bar_chart_waste_treat, name='horizontal_bar_chart_waste_treat'),
    #path('pie_chart_waste_dim/', pie_chart_waste_dim, name='pie_chart_waste_dim'),
    
    # Employment
    #path('line_chart_employment_rate/', line_chart_employment_rate, name='line_chart_employment_rate'),
    #path('bar_chart_employment_ranking/', bar_chart_employment_ranking, name='bar_chart_employment_ranking'),
    #path('donut_chart_employment_by_sex/', donut_chart_employment_by_sex, name='donut_chart_employment_by_sex'),
    
    # Resilience dashboard
    path('bar_chart_total_pop_ranking/', bar_chart_total_pop_ranking, name='bar_chart_total_pop_ranking'),
    path('bar_chart_pop_aged_ranking/', bar_chart_pop_aged_ranking, name='bar_chart_pop_aged_ranking'),
    path('line_chart_tertiary_educ_attain/', line_chart_tertiary_educ_attain, name='line_chart_tertiary_educ_attain'),
    path('grouped_bar_chart_pop_by_age_group/', grouped_bar_chart_pop_by_age_group, name='grouped_bar_chart_pop_by_age_group'),
    path('line_chart_by_resilience_kpis/', line_chart_by_resilience_kpis, name='line_chart_by_resilience_kpis'),
    path('grouped_bar_chart_physi_vs_hosp_beds/', grouped_bar_chart_physi_vs_hosp_beds, name='grouped_bar_chart_physi_vs_hosp_beds'),
]