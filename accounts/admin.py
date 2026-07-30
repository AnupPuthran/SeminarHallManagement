from django.contrib import admin
from .models import SeminarHall, Booking


@admin.register(SeminarHall)
class SeminarHallAdmin(admin.ModelAdmin):
    list_display = ('hall_name', 'capacity', 'location')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'hall',
        'booking_date',
        'start_time',
        'end_time',
        'status'
    )

    list_editable = ('status',)