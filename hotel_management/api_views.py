from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from django.utils.translation import gettext_lazy as _

from hotel_management.models import Reservation
from hotel_management.serializers import ReservationSerializer, ReservationUpdateSerializer
from users.models import ManagerProfile

from permissions.decorators import required_permission


class ManagerReservationsListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    @required_permission('HMAN_RES', 'READ')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        managed_hotels = user.managed_hotels.all().values_list('hotel', flat=True)

        # return no reservations if no hotels are managed
        if not managed_hotels:
            return Reservation.objects.none()

        return Reservation.objects.filter(room__hotel__in=managed_hotels)


class ReservationUpdateView(generics.UpdateAPIView):
    serializer_class = ReservationUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Reservation.objects.all()

    def get_object(self):
        return Reservation.objects.get(pk=self.kwargs['pk'])
