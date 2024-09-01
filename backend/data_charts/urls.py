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
    path('line_chart_waste/', line_chart_waste, name='line_chart_waste'),
    path('line_chart_waste_recycled/', line_chart_waste_recycled, name='line_chart_waste_recycled'),
    path('bar_chart_waste_recycled/', bar_chart_waste_recycled, name='bar_chart_waste_recycled'),
    path('donut_chart_waste/', donut_chart_waste, name='donut_chart_waste'),
    
    # Employment
    path('line_chart_employment/', line_chart_employment, name='line_chart_employment'),
    path('donut_chart_employment/', donut_chart_employment, name='donut_chart_employment'),
    
    # Infrastructure
    path('line_chart_infrastructure/', line_chart_infrastructure, name="line_chart_infrastructure"),
    path('bar_chart_infrastructure/', bar_chart_infrastructure, name="bar_chart_infrastructure"),
    
    # Innovation
    path('line_chart_innovation/', line_chart_innovation, name="line_chart_innovation"),
    path('grouped_bar_chart_innovation/', grouped_bar_chart_innovation, name="grouped_bar_chart_innovation"),
    
    # Health
    path('line_chart_health/', line_chart_health, name="line_chart_health"),
    path('bar_chart_health/', bar_chart_health, name="bar_chart_health"),
    
    # Safety
    path('line_chart_safety/', line_chart_safety, name="line_chart_safety"),
    path('bar_chart_safety/', bar_chart_safety, name="bar_chart_safety"),
    
    # Education
    path('line_chart_education/', line_chart_education, name="line_chart_education"),
    path('bar_chart_education/', bar_chart_education, name="bar_chart_education"),
    
    # Social Resilience dashboard
    
    path('line_chart_social_resilience/', line_chart_social_resilience, name='line_chart_social_resilience'),
        # Educational equality
    path('bar_chart_educational_equality_by_sex/', bar_chart_educational_equality_by_sex, name='bar_chart_educational_equality_by_sex'),
        # Demography
    path('donut_chart_demo_pop_productive_age/', donut_chart_demo_pop_productive_age, name='donut_chart_demo_pop_productive_age'),
    path('donut_chart_demo_pop_aged_65/', donut_chart_demo_pop_aged_65, name='donut_chart_demo_pop_aged_65'),
    path('bar_chart_demo_pop_density/', bar_chart_demo_pop_density, name='bar_chart_demo_pop_density'),
        # Transportation access
    path('donut_chart_transportation_access/', donut_chart_transportation_access, name='donut_chart_transportation_access'),
    path('grouped_bar_chart_transportation_access/', grouped_bar_chart_transportation_access, name='grouped_bar_chart_transportation_access'),
]