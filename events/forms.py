
from django import forms
from .models import Event, Venue, Resource


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "event_type",
            "description",
            "event_date",
            "start_time",
            "end_time",
            "expected_attendees",
            "budget",
            "venue",
        ]

        widgets = {
            "event_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "start_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
            "end_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 3}
            ),
            "expected_attendees": forms.NumberInput(
                attrs={"min": 1}
            ),
            "budget": forms.NumberInput(
                attrs={"min": 0, "step": "0.01"}
            ),
        }

        labels = {
            "venue": "Venue",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["venue"].required = False
        self.fields["venue"].empty_label = "Select a venue (optional)"
        self.fields["venue"].queryset = Venue.objects.order_by("name")

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get("start_time")
        end = cleaned_data.get("end_time")
        attendees = cleaned_data.get("expected_attendees")

        if start and end and end <= start:
            self.add_error(
                "end_time",
                "End time must be later than start time.",
            )

        if attendees is not None and attendees < 1:
            self.add_error(
                "expected_attendees",
                "Expected attendees must be at least 1.",
            )

        return cleaned_data


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = [
            "name",
            "venue_type",
            "address",
            "city",
            "capacity",
            "rental_cost",
            "is_available",
            "description",
        ]

        widgets = {
            "address": forms.Textarea(
                attrs={"rows": 3}
            ),
            "capacity": forms.NumberInput(
                attrs={"min": 1}
            ),
            "rental_cost": forms.NumberInput(
                attrs={"min": 0, "step": "0.01"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 3}
            ),
        }

    def clean_capacity(self):
        capacity = self.cleaned_data["capacity"]

        if capacity < 1:
            raise forms.ValidationError(
                "Venue capacity must be at least 1."
            )

        return capacity

    def clean_rental_cost(self):
        rental_cost = self.cleaned_data["rental_cost"]

        if rental_cost < 0:
            raise forms.ValidationError(
                "Rental cost cannot be negative."
            )

        return rental_cost


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            "name",
            "category",
            "quantity",
            "unit_cost",
            "is_available",
            "description",
        ]

        widgets = {
            "quantity": forms.NumberInput(
                attrs={"min": 1}
            ),
            "unit_cost": forms.NumberInput(
                attrs={"min": 0, "step": "0.01"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 3}
            ),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if quantity < 1:
            raise forms.ValidationError(
                "Quantity must be at least 1."
            )
        return quantity

    def clean_unit_cost(self):
        unit_cost = self.cleaned_data["unit_cost"]
        if unit_cost < 0:
            raise forms.ValidationError(
                "Unit cost cannot be negative."
            )
        return unit_cost

