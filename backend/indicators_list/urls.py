from django.urls import path
from .views import indicators_check_list

urlpatterns = [
    path('indicators_check_list/', indicators_check_list, name='indicators_check_list'),
]