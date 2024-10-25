from django.urls import path

from .api_views import ManagerReservationsListView, ReservationUpdateView


app_name = 'hotel_management_api'

urlpatterns = [
    path('reservation/for-manager/get/all/', ManagerReservationsListView.as_view(), name='reservations-for-manager'),
    path('reservation/state/update/<int:pk>/', ReservationUpdateView.as_view(), name='reservations-update')
]