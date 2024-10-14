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
    
    # Sustainability dashboard
    
    # Air quality
    path('bar_chart_GHG/', bar_chart_GHG, name='bar_chart_GHG'),
    path('bar_chart_air_quality/', bar_chart_air_quality, name="bar_chart_air_quality"),
    path('card_air_quality/', card_air_quality, name='card_air_quality'),
    path('line_chart_GHG/', line_chart_GHG, name='line_chart_GHG'),
    
    # Energy
    path('line_chart_energy/', line_chart_energy, name='line_chart_energy'),
    path('bar_chart_energy/', bar_chart_energy, name='bar_chart_energy'),
    path('donut_chart_energy/', donut_chart_energy, name='donut_chart_energy'),
    
    # Biodiversity
    path('bar_chart_TPA_prot_area/', bar_chart_TPA_prot_area, name='bar_chart_TPA_prot_area'),
    
    # Environmental quality
    path('line_chart_waste_recycled/', line_chart_waste_recycled, name='line_chart_waste_recycled'),
    path('bar_chart_waste_recycled/', bar_chart_waste_recycled, name='bar_chart_waste_recycled'),
    path('donut_chart_waste_recycled/', donut_chart_waste_recycled, name='donut_chart_waste_recycled'),
    
    # Employment
    path('line_chart_employment/', line_chart_employment, name='line_chart_employment'),
    path('bar_chart_employment/', bar_chart_employment, name='bar_chart_employment'),
    path('stacked_bar_chart_employment/', stacked_bar_chart_employment, name='stacked_bar_chart_employment'),
    
    # Health
    path('line_chart_health/', line_chart_health, name="line_chart_health"),
    path('bar_chart_health/', bar_chart_health, name="bar_chart_health"),
    
    # Safety
    path('line_chart_safety/', line_chart_safety, name="line_chart_safety"),
    path('bar_chart_safety/', bar_chart_safety, name="bar_chart_safety"),
    
    # Education
    path('line_chart_education/', line_chart_education, name="line_chart_education"),
    path('bar_chart_education/', bar_chart_education, name="bar_chart_education"),
    
    # Resilience dashboard
    
    # Educational equality
    path('bar_chart_educational_equality_by_sex/', bar_chart_educational_equality_by_sex, name='bar_chart_educational_equality_by_sex'),
    
    # Demography
    path('donut_chart_demo_pop_productive_age/', donut_chart_demo_pop_productive_age, name='donut_chart_demo_pop_productive_age'),
    path('donut_chart_demo_pop_aged_65/', donut_chart_demo_pop_aged_65, name='donut_chart_demo_pop_aged_65'),
    path('bar_chart_demo_pop_density/', bar_chart_demo_pop_density, name='bar_chart_demo_pop_density'),
    
    # Transportation access
    path('donut_chart_transportation_access/', donut_chart_transportation_access, name='donut_chart_transportation_access'),
    
    # Economic Resilience
    path('line_chart_economic_resilience/', line_chart_economic_resilience, name="line_chart_economic_resilience"),
    path('bar_chart_economic_resilience/', bar_chart_economic_resilience, name="bar_chart_economic_resilience"),
    
    # Infrastructure Resilience
    path('line_chart_infrastructure_resilience/', line_chart_infrastructure_resilience, name="line_chart_infrastructure_resilience"),
    path('bar_chart_infrastructure_resilience/', bar_chart_infrastructure_resilience, name="bar_chart_infrastructure_resilience"),

    # Hazard Resilience dashboard
    
    # Institutional Resilience dashboard
    path('line_chart_institutional_resilience/', line_chart_institutional_resilience, name="line_chart_institutional_resilience"),
    path('bar_chart_institutional_resilience/', bar_chart_institutional_resilience, name="bar_chart_institutional_resilience")
]