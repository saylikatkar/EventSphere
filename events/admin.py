
from django.contrib import admin
from .models import Event, Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "venue_type",
        "city",
        "capacity",
        "rental_cost",
        "is_available",
    )
    list_filter = ("venue_type", "city", "is_available")
    search_fields = ("name", "city", "address")
    list_editable = ("is_available",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "event_type",
        "event_date",
        "start_time",
        "end_time",
        "venue",
        "expected_attendees",
    )
    list_filter = ("event_type", "event_date")
    search_fields = ("name",)
