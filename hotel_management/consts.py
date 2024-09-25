from django.utils.translation import gettext_lazy as _


RESERVATION_STATUS_PENDING = 'pending'
RESERVATION_STATUS_CONFIRMED = 'confirmed'
RESERVATION_STATUS_CANCELED = 'canceled'
RESERVATION_STATUS_COMPLETED = 'completed'

RESERVATION_STATUSES = [
    (RESERVATION_STATUS_PENDING, _('Pending')),
    (RESERVATION_STATUS_CONFIRMED, _('Confirmed')),
    (RESERVATION_STATUS_CANCELED, _('Canceled')),
    (RESERVATION_STATUS_COMPLETED, _('Completed')),
]

ROOM_TYPE_SINGLE = 'single'
ROOM_TYPE_DOUBLE = 'double'
ROOM_TYPE_SUITE = 'suite'
ROOM_TYPE_DELUXE = 'deluxe'
ROOM_TYPE_FAMILY = 'family'

ROOM_TYPES = [
    (ROOM_TYPE_SINGLE, _('Single')),
    (ROOM_TYPE_DOUBLE, _('Double')),
    (ROOM_TYPE_SUITE, _('Suite')),
    (ROOM_TYPE_DELUXE, _('Deluxe')),
    (ROOM_TYPE_FAMILY, _('Family')),
]