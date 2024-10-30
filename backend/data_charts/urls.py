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
    
    # Environmental Sustainability
        # Air quality
    path('bar_chart_GHG/', bar_chart_GHG, name='bar_chart_GHG'),
    path('bar_chart_air_quality/', bar_chart_air_quality, name="bar_chart_air_quality"),
    path('card_air_quality/', card_air_quality, name='card_air_quality'),
    path('line_chart_GHG/', line_chart_GHG, name='line_chart_GHG'),
    
        # Energy
    path('line_chart_energy/', line_chart_energy, name='line_chart_energy'),
    path('bar_chart_energy/', bar_chart_energy, name='bar_chart_energy'),
    
        # Biodiversity
    path('bar_chart_TPA_prot_area/', bar_chart_TPA_prot_area, name='bar_chart_TPA_prot_area'),
    
        # Environmental quality
    path('line_chart_waste_recycled/', line_chart_waste_recycled, name='line_chart_waste_recycled'),
    path('bar_chart_waste_recycled/', bar_chart_waste_recycled, name='bar_chart_waste_recycled'),
    path('donut_chart_waste_recycled/', donut_chart_waste_recycled, name='donut_chart_waste_recycled'),
    
    # Economic Sustainability
    path('line_chart_economic_sustainability/', line_chart_economic_sustainability, name='line_chart_economic_sustainability'),
    path('bar_chart_economic_sustainability/', bar_chart_economic_sustainability, name='bar_chart_economic_sustainability'),
    
    # Social Sustainability
    path('line_chart_social_sustainability/', line_chart_social_sustainability, name="line_chart_social_sustainability"),
    path('bar_chart_social_sustainability/', bar_chart_social_sustainability, name="bar_chart_social_sustainability"),
    
    # Resilience dashboard
    
    # Social Resilience
        # Educational equality
    path('line_chart_educational_equality/', line_chart_educational_equality, name='line_chart_educational_equality'),
    path('bar_chart_educational_equality/', bar_chart_educational_equality, name='bar_chart_educational_equality'),
    
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
    
    # Institutional Resilience dashboard
    path('line_chart_institutional_resilience/', line_chart_institutional_resilience, name="line_chart_institutional_resilience"),
    path('bar_chart_institutional_resilience/', bar_chart_institutional_resilience, name="bar_chart_institutional_resilience")
]