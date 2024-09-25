from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from hotel_management.models import Hotel, Room, Reservation


# Register your models here.

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "country", "state", "city", "address"]
    list_display_links = ["pk", ]
    list_filter = ["rating", "country"]
    fieldsets = (
        ("Informacje", {"fields": ("rating", "name")}),
        ("Lokalizacja", {"fields": ("country", "state", "city", "address")}),
        ("Kontakt", {"fields": ("phone", "email")}),
    )
    empty_value_display = "-empty-"

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ["pk", "hotel_name", "room_number", "room_type", "price_per_night", "is_available"]
    list_display_links = ["pk", ]
    list_select_related = ('hotel',)
    list_filter = ["hotel", "room_type", "bed_count", "capacity"]
    fieldsets = (
        ("Parametry", {"fields": ("hotel", "room_number", "room_type")}),
        ("Pojemność", {"fields": ("bed_count", "capacity")}),
        ("Dodatkowe informacje", {"fields": ("price_per_night", "amenities", "description")}),
    )
    empty_value_display = "-empty-"

    @admin.display(description='Hotel')
    def hotel_name(self, obj):
        return obj.hotel.name


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["pk", "hotel_name_link", "room_number_link", "guest_full_name", "check_in_date", "check_out_date", "number_of_guests", "reservation_status"]
    list_display_links = ["pk", "hotel_name_link", "room_number_link"]
    list_select_related = ('room', "guest")
    list_filter = ["number_of_guests", "reservation_status"]
    fieldsets = (
        ("Informacje", {"fields": ("room", "guest", "number_of_guests", "special_requests")}),
        ("Czas wynajmu", {"fields": ("check_in_date", "check_out_date")}),
        ("Status", {"fields": ("reservation_status",)}),
    )
    empty_value_display = "-empty-"

    @admin.display(description="Hotel")
    def hotel_name_link(self, obj):
        return format_html('<a href="{}">{}</a>',
                           reverse('admin:hotel_management_hotel_change', args=[obj.room.hotel.pk]),
                           obj.room.hotel.name)

    @admin.display(description="Rodzaj pokoju")
    def room_number_link(self, obj):
        return format_html('<a href="{}">{}</a>',
                           reverse('admin:hotel_management_room_change', args=[obj.room.pk]),
                           obj.room.room_type)

    @admin.display(description='Imię i nazwisko gościa')
    def guest_full_name(self, obj):
        return f'{obj.guest.first_name} {obj.guest.last_name}'