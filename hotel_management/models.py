from django.utils import timezone

from django.core.validators import validate_email, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q, UniqueConstraint

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from dicts.models import BaseModel
from dicts.validators import validate_phone_number
from hotel_management.consts import RESERVATION_STATUSES, RESERVATION_STATUS_PENDING, ROOM_TYPES
from hotel_management.managers import ReservationManager
from users.models import ClientProfile, ManagerProfile


class Hotel(BaseModel):
    rating = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Ocena'), help_text=_('Ocena hotelu'))
    name = models.CharField(
        max_length=124,
        unique=True,
        verbose_name=_("Nazwa"), help_text=_("Nazwa hotelu"))
    address = models.CharField(
        max_length=124,
        verbose_name=_("Adres"), help_text=_("Adres hotelu"))
    city = models.CharField(
        max_length=124,
        verbose_name=_("Miasto"), help_text=_("Miasto hotelu"))
    state = models.CharField(
        max_length=124,
        verbose_name=_("Region"), help_text=_("Region hotelu"))
    country = models.CharField(
        max_length=124,
        verbose_name=_("Kraj"), help_text=_("Kraj hotelu"))
    phone = models.CharField(
        max_length=32,
        validators=[validate_phone_number],
        unique=True,
        verbose_name=_("Numer telefonu"), help_text=_("Numer telefonu recepcji hotelu"))
    email = models.EmailField(
        max_length=124,
        validators=[validate_email],
        verbose_name=_("Adres email"), help_text=_("Adres email recepcji hotelu"))

    def __str__(self):
        return f'Hotel {self.name} - {self.city}'

    def __repr__(self):
        return f"<Hotel(id={self.id}, name={self.name}, address={self.address}, rating={self.rating})>"

    class Meta:
        ordering = ["rating"]
        get_latest_by = "-created_at"
        verbose_name = _("Hotel")
        verbose_name_plural = _("Hotele")
        db_table = "hotels"


class Room(BaseModel):
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name=_("Hotel"), help_text=_("Hotel"))
    room_number = models.PositiveSmallIntegerField(
        unique=True,
        verbose_name=_("Numer pokoju"), help_text=_("Numer pokoju"))
    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPES,
        verbose_name=_("Typ pokoju"), help_text=_("Typ pokoju"))
    bed_count = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name=_("Liczba łóżek"), help_text=_("Liczba łóżek w pokoju"))
    capacity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("Maksymalna pojemność"), help_text=_("Maksymalna pojemność pokoju"))
    price_per_night = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Cena za noc"), help_text=_("Cena za noc w pokoju"))
    is_available = models.BooleanField(
        default=True,
        verbose_name=_("Czy dostępny"), help_text=_("Czy pokój dostępny"))
    amenities = models.TextField(
        blank=True,
        verbose_name=_("Udogodnienia"), help_text=_("Udogodnienia w pokoju"))
    description = models.TextField(
        max_length=1024,
        blank=True,
        verbose_name=_("Opis"), help_text=_("Opis pokoju"))

    def is_available_in_range(self, start_date, end_date):
        """
        returns bool response depending on availability of the room at the given time period
        """
        return not self.reservations.filter(check_in_date__lte=end_date, check_out_date__gte=start_date).exists()

    def __str__(self):
        return f'Room: ({self.room_number}) - {self.room_type}'

    def __repr__(self):
        return f"<Room(id={self.id}, hotel={self.hotel.name}, room_number={self.room_number})>"

    class Meta:
        ordering = ["room_number"]
        get_latest_by = "-created_at"
        verbose_name = _("Pokój")
        verbose_name_plural = _("Pokoje")
        db_table = "rooms"


class Reservation(BaseModel):
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name='reservations',
        verbose_name=_("Pokój"), help_text=_("Pokój na rezerwacji"))
    guest = models.ForeignKey(
        ClientProfile,
        on_delete=models.PROTECT,
        related_name='reservations',
        verbose_name=_("Gość"), help_text=_("Gość na rezerwacji")
    )
    check_in_date = models.DateField(
        verbose_name=_("Data rozpoczęcia"), help_text=_("Data rozpoczęcia rezerwacji")
    )
    check_out_date = models.DateField(
        blank=True, null=True,
        verbose_name=_("Data zakończenia"), help_text=_("Data zakończenia rezerwacji")
    )
    number_of_guests = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name=_("Liczba gości"), help_text=_("Liczba gości na rezerwacji")
    )
    reservation_status = models.CharField(
        max_length=20,
        choices=RESERVATION_STATUSES,
        default='pending',
        verbose_name=_("Status"), help_text=_("Status rezerwacji")
    )
    special_requests = models.TextField(
        blank=True, null=True,
        max_length=1024,
        verbose_name=_("Specjalne wymagania"), help_text=_("Specjalne wymagania")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Czy aktywna rezerwacja"), help_text=_("Czy aktywna rezerwacja")
    )

    objects = ReservationManager()

    def __str__(self):
        return f'Reservation {self.guest} - {self.room}'

    def __repr__(self):
        return f"<Reservation(id={self.id}, room={self.room.room_type}, guest={self.guest.full_name})>"

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get("check_in_date")
        check_out_date = cleaned_data.get("check_out_date")

        if check_in_date and check_out_date:
            actual_date = timezone.now().date()

            # check that check-in and check-out dates are not in the past
            if check_in_date < actual_date or check_out_date < actual_date:
                raise ValidationError(_("Provided check-in and check-out dates cannot be in the past"))

            # check that check-out date is greater than check-in date
            if check_in_date >= check_in_date:
                raise ValidationError(_("Check-in date cannot be greater or equal to check-out date"))

            # check availability of the room in the given date range
            if not cleaned_data.room.is_available_in_range(check_in_date, check_out_date):
                raise ValidationError(_("Room is not available at given date range"))


    class Meta:
        ordering = ["-check_in_date", "-check_out_date"]
        get_latest_by = "-created_at"
        verbose_name = _("Rezerwacja")
        verbose_name_plural = _("Rezerwacje")
        db_table = "reservations"
        constraints = [
            UniqueConstraint(
                fields=['room'],
                condition=Q(room__is_available=True),
                name='unique_active_reservation_per_room'
            )
        ]

class HotelManagerAssignment(BaseModel):
    manager = models.ForeignKey(
        ManagerProfile,
        on_delete=models.CASCADE,
        related_name="managed_hotels",
        verbose_name=_("Menadżer"), help_text=_("Menadżer hotelu"))
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="managers",
        verbose_name=_("Hotel"), help_text=_("Hotel podlegający pod menadżera"))

    def __str__(self):
        return f"HotelManagerRelation {self.manager} -> {self.hotel}"

    def __repr__(self):
        return f"<HotelManagerRelation(id={self.pk}, manager={self.manager}, hotel={self.hotel})>"

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = "-created_at"
        verbose_name = _("Przypisanie menadżera do hotelu")
        verbose_name_plural = _("Przypisania menadżerów do hoteli")
        unique_together = ('manager', 'hotel')
        db_table = "hotel_to_manager"