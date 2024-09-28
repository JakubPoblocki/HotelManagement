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

    # @required_permission('HMAN_RES', 'READ')
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        user = ''
        # user = self.request.user
        if not user:
            user = ManagerProfile.objects.get(pk=1)
        if not isinstance(user, ManagerProfile):
            raise ValueError(_("ERROR_WRONG_USER_PERMISSIONS"))

        managed_hotels = user.managed_hotels.all().values_list('hotel', flat=True)
        if not managed_hotels:
            return Reservation.objects.all()

        return Reservation.objects.filter(room__hotel__in=managed_hotels)


class ReservationUpdateView(generics.UpdateAPIView):
    serializer_class = ReservationUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Reservation.objects.get(pk=self.kwargs['pk'])
