from django.db import models

from .consts import RESERVATION_STATUS_PENDING
# from rest_framework.exceptions import ValidationError


class ReservationManager(models.Manager):
    def create(self, **extra_fields):
        reservation = self.model(reservation_status=RESERVATION_STATUS_PENDING, **extra_fields)
        reservation.full_clean()
        reservation.save()
        return reservation