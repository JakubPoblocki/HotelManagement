from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from hotel_management.consts import ROOM_TYPES, RESERVATION_STATUSES, STATUS_TRANSITIONS
from hotel_management.models import Reservation, Hotel, Room
from users.serializers import ClientProfileSerializer


class HotelSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Hotel model
    """
    rating = serializers.IntegerField(
        read_only=True,
        help_text=_("Ocena"))
    name = serializers.CharField(
        read_only=True,
        help_text=_("Nazwa"))
    address = serializers.CharField(
        read_only=True,
        help_text=_("Adres"))
    city = serializers.CharField(
        read_only=True,
        help_text=_("Miasto"))
    state = serializers.CharField(
        read_only=True,
        help_text=_("Region"))
    country = serializers.CharField(
        read_only=True,
        help_text=_("Kraj"))
    phone = serializers.CharField(
        read_only=True,
        help_text=_("Numer telefonu"))
    email = serializers.EmailField(
        read_only=True,
        help_text=_("Email"))

    class Meta:
        model = Hotel
        fields = ['pk',
                  'rating',
                  'name',
                  'address',
                  'city',
                  'state',
                  'country',
                  'phone',
                  'email']


class RoomDetailedSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Room model
    """
    hotel = HotelSerializer(
        read_only=True,
        help_text=_('Szczegóły hotelu'))
    room_number = serializers.IntegerField(
        read_only=True,
        help_text=_("Numer pokoju"))
    room_type = serializers.ChoiceField(
        read_only=True,
        choices=ROOM_TYPES,
        help_text=_("Typ pokoju"))
    bed_count = serializers.IntegerField(
        read_only=True,
        help_text=_("Liczba łóżek"))
    capacity = serializers.IntegerField(
        read_only=True,
        help_text=_("Liczba miejsc"))
    price_per_night = serializers.IntegerField(
        read_only=True,
        help_text=_("Cena za noc"))
    is_available = serializers.BooleanField(
        read_only=True,
        help_text=_("Czy dostępny"))
    amenities = serializers.CharField(
        read_only=True,
        help_text=_("Udogodnienia"))
    description = serializers.CharField(
        read_only=True,
        help_text=_("Opis"))

    class Meta:
        model = Room
        fields = ['pk',
                  'hotel',
                  'room_number',
                  'room_type',
                  'bed_count',
                  'capacity',
                  'price_per_night',
                  'is_available',
                  'amenities',
                  'description']


class ReservationSerializer(serializers.ModelSerializer):
    """
    Base serializer for Reservation model
    """
    room = serializers.IntegerField(
        source="room.id",
        read_only=True,
        help_text=_("Hotel"))
    guest = serializers.IntegerField(
        source="guest.id",
        read_only=True,
        help_text=_("Gość"))
    check_in_date = serializers.DateField(
        read_only=True,
        help_text=_("Data rozpoczęcia rezerwacji"))
    check_out_date = serializers.DateField(
        read_only=True,
        help_text=_("Data zakończenia rezerwacji"))
    number_of_guests = serializers.IntegerField(
        read_only=True,
        help_text=_("Liczba gości"))
    reservation_status = serializers.ChoiceField(
        read_only=True,
        choices=RESERVATION_STATUSES,
        help_text=_("Liczba rezerwacji"))
    special_requests = serializers.CharField(
        read_only=True,
        help_text=_("Specjalne wymagania"))
    is_active = serializers.BooleanField(
        read_only=True,
        help_text=_("Czy aktywna"))

    class Meta:
        model = Reservation
        fields = ['pk',
                  'room',
                  'guest',
                  'check_in_date',
                  'check_out_date',
                  'number_of_guests',
                  'reservation_status',
                  'special_requests',
                  'is_active']


class ReservationDetailedSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Reservation model
    """
    room = RoomDetailedSerializer(
        read_only=True,
        help_text=_("Pokój na rezerwacji"))
    guest = ClientProfileSerializer(
        read_only=True,
        help_text=_("Gość na rezerwacji"))
    check_in_date = serializers.DateField(
        read_only=True,
        help_text=_("Data rozpoczęcia rezerwacji"))
    check_out_date = serializers.DateField(
        read_only=True,
        help_text=_("Data zakończenia rezerwacji"))
    number_of_guests = serializers.IntegerField(
        read_only=True,
        help_text=_("Liczba gości"))
    reservation_status = serializers.ChoiceField(
        read_only=True,
        choices=RESERVATION_STATUSES,
        help_text=_("Liczba rezerwacji"))
    special_requests = serializers.CharField(
        read_only=True,
        help_text=_("Specjalne wymagania"))
    is_active = serializers.BooleanField(
        read_only=True,
        help_text=_("Czy aktywna"))

    class Meta:
        model = Reservation
        fields = ['pk',
                  'room',
                  'guest',
                  'check_in_date',
                  'check_out_date',
                  'number_of_guests',
                  'reservation_status',
                  'special_requests',
                  'is_active']


class ReservationUpdateSerializer(serializers.ModelSerializer):
    """
    Update serializer for Reservation status
    """
    room = RoomDetailedSerializer(
        required=False,
        allow_null=True,
        help_text=_("Pokój na rezerwacji"))
    guest = ClientProfileSerializer(
        required=False,
        allow_null=True,
        help_text=_("Gość na rezerwacji"))
    check_in_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text=_("Data rozpoczęcia rezerwacji"))
    check_out_date = serializers.DateField(
        required=False,
        allow_null=True,
        help_text=_("Data zakończenia rezerwacji"))
    number_of_guests = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text=_("Liczba gości"))
    reservation_status = serializers.ChoiceField(
        required=False,
        allow_null=True,
        choices=RESERVATION_STATUSES,
        help_text=_("Status"))
    special_requests = serializers.CharField(
        required=False,
        allow_null=True,
        help_text=_("Specjalne wymagania"))
    is_active = serializers.BooleanField(
        required=False,
        allow_null=True,
        help_text=_("Czy aktywna"))

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def validate_reservation_status(self, value):
        current_status = self.instance.reservation_status
        valid_transitions = STATUS_TRANSITIONS.get(current_status, [])

        if value not in valid_transitions:
            raise serializers.ValidationError(f"Invalid transition from {current_status} to {value}.")
        return value

    class Meta:
        model = Reservation
        fields = ['pk',
                  'room',
                  'guest',
                  'check_in_date',
                  'check_out_date',
                  'number_of_guests',
                  'reservation_status',
                  'special_requests',
                  'is_active']