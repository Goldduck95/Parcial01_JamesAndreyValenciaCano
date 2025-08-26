from django.urls import path
from .views import (
    HomePageView, 
    FlightCreateView, 
    FlightSuccessView,
    FlightListView, 
    FlightStatsView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('flights/create/', FlightCreateView.as_view(), name='flight_create'),
    path('flights/success/', FlightSuccessView.as_view(), name='flight_success'),
    path('flights/list/', FlightListView.as_view(), name='flight_list'),
    path('flights/stats/', FlightStatsView.as_view(), name='flight_stats'),
]

