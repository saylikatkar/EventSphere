
from django.core.exceptions import ValidationError
from django.db import models


class Venue(models.Model):
    VENUE_TYPES = [
        ("Auditorium", "Auditorium"),
        ("Conference Hall", "Conference Hall"),
        ("Banquet Hall", "Banquet Hall"),
        ("Outdoor", "Outdoor"),
        ("Classroom", "Classroom"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=200)
    venue_type = models.CharField(
        max_length=30,
        choices=VENUE_TYPES,
        default="Other",
    )
    address = models.TextField()
    city = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    rental_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.city}"


class Event(models.Model):
    EVENT_TYPES = [
        ("Technical", "Technical"),
        ("Cultural", "Cultural"),
        ("Workshop", "Workshop"),
        ("Conference", "Conference"),
        ("Sports", "Sports"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=200)
    event_type = models.CharField(
        max_length=30,
        choices=EVENT_TYPES,
        default="Other",
    )
    description = models.TextField(blank=True)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    expected_attendees = models.PositiveIntegerField(default=0)
    budget = models.DecimalField(max_digits=12, decimal_places=2)

    # A venue can host multiple events at different times.
    # Existing events can remain unassigned.
    venue = models.ForeignKey(
        Venue,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["event_date", "start_time"]

    def clean(self):
        super().clean()

        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError({
                    "end_time": "End time must be later than start time."
                })

        if not self.venue_id or not self.event_date:
            return

        if not self.venue.is_available:
            raise ValidationError({
                "venue": "This venue is currently marked unavailable."
            })

        if self.expected_attendees > self.venue.capacity:
            raise ValidationError({
                "venue": (
                    f"This venue accommodates {self.venue.capacity} people, "
                    f"but your event expects {self.expected_attendees}."
                )
            })

        if not self.start_time or not self.end_time:
            return

        # Detect overlapping events assigned to this venue.
        overlapping_events = Event.objects.filter(
            venue_id=self.venue_id,
            event_date=self.event_date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(pk=self.pk)

        if overlapping_events.exists():
            raise ValidationError({
                "venue": "This venue already has an event scheduled during this time."
            })

    def __str__(self):
        return self.name


class Resource(models.Model):
    RESOURCE_CATEGORIES = [
        ("Audio", "Audio Equipment"),
        ("Visual", "Visual Equipment"),
        ("Furniture", "Furniture"),
        ("Electronics", "Electronics"),
        ("Stationery", "Stationery"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=30,
        choices=RESOURCE_CATEGORIES,
        default="Other",
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
