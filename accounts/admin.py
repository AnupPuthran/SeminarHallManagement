from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
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
        'status',
    )
    list_editable = ('status',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.user.email:
            if obj.status == "Approved":
                send_mail(
                    "Seminar Hall Booking Approved",
                    f"Hello {obj.user.username},\n\n"
                    f"Your booking for '{obj.hall}' has been approved.\n\n"
                    f"Date: {obj.booking_date}\n"
                    f"Time: {obj.start_time} - {obj.end_time}\n\n"
                    f"Thank you.",
                    settings.DEFAULT_FROM_EMAIL,
                    [obj.user.email],
                    fail_silently=True,
                )

            elif obj.status == "Rejected":
                send_mail(
                    "Seminar Hall Booking Rejected",
                    f"Hello {obj.user.username},\n\n"
                    f"Your booking for '{obj.hall}' has been rejected.\n\n"
                    f"Date: {obj.booking_date}\n"
                    f"Time: {obj.start_time} - {obj.end_time}\n\n"
                    f"Thank you.",
                    settings.DEFAULT_FROM_EMAIL,
                    [obj.user.email],
                    fail_silently=True,
                )