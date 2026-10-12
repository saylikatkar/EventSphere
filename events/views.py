
from datetime import date
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EventForm, VenueForm, ResourceForm
from .models import Event, Venue, Resource


# -------------------------
# Dashboard
# -------------------------

def dashboard(request):
    today = date.today()

    events = Event.objects.select_related("venue").all()
    edit_id = request.GET.get("edit")

    edit_event = (
        events.filter(pk=edit_id).first()
        if edit_id
        else events.first()
    )

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create":
            create_form = EventForm(request.POST)

            if create_form.is_valid():
                create_form.save()
                messages.success(request, "Event created successfully.")
                return redirect("dashboard")

            edit_form = EventForm(instance=edit_event)

        elif action == "update" and edit_event:
            edit_form = EventForm(request.POST, instance=edit_event)

            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, "Event updated successfully.")
                return redirect("dashboard")

            create_form = EventForm()

        else:
            create_form = EventForm()
            edit_form = EventForm(instance=edit_event)

    else:
        create_form = EventForm()
        edit_form = EventForm(instance=edit_event)

    context = {
        "events": events,
        "today": today,
        "total_events": events.count(),
        "upcoming_events": events.filter(event_date__gte=today).count(),
        "available_venues": Venue.objects.filter(is_available=True).count(),
        "total_venues": Venue.objects.count(),
        "total_resources": Resource.objects.count(),
        "create_form": create_form,
        "edit_form": edit_form,
        "edit_event": edit_event,
    }

    return render(request, "events/dashboard.html", context)


# -------------------------
# Event pages
# -------------------------

def event_list(request):
    events = Event.objects.select_related("venue").all()

    return render(
        request,
        "events/event_list.html",
        {"events": events},
    )


def event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.select_related("venue"),
        pk=pk,
    )

    return render(
        request,
        "events/event_detail.html",
        {"event": event},
    )


def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save()
            messages.success(request, "Event created successfully.")
            return redirect("event_detail", pk=event.pk)
    else:
        form = EventForm()

    return render(
        request,
        "events/event_form.html",
        {"form": form, "page_title": "Create Event"},
    )


def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)

        if form.is_valid():
            event = form.save()
            messages.success(request, "Event updated successfully.")
            return redirect("event_detail", pk=event.pk)
    else:
        form = EventForm(instance=event)

    return render(
        request,
        "events/event_form.html",
        {"form": form, "page_title": "Edit Event"},
    )


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully.")
        return redirect("event_list")

    return render(
        request,
        "events/event_confirm_delete.html",
        {"event": event},
    )


# -------------------------
# Venue management
# -------------------------

def venue_list(request):
    venues = Venue.objects.all()

    return render(
        request,
        "events/venue_list.html",
        {"venues": venues},
    )


def venue_create(request):
    if request.method == "POST":
        form = VenueForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Venue added successfully.")
            return redirect("venue_list")
    else:
        form = VenueForm()

    return render(
        request,
        "events/venue_form.html",
        {"form": form, "page_title": "Add Venue"},
    )


def venue_update(request, pk):
    venue = get_object_or_404(Venue, pk=pk)

    if request.method == "POST":
        form = VenueForm(request.POST, instance=venue)

        if form.is_valid():
            form.save()
            messages.success(request, "Venue updated successfully.")
            return redirect("venue_list")
    else:
        form = VenueForm(instance=venue)

    return render(
        request,
        "events/venue_form.html",
        {"form": form, "page_title": "Edit Venue"},
    )


def venue_delete(request, pk):
    venue = get_object_or_404(Venue, pk=pk)

    if request.method == "POST":
        venue.delete()
        messages.success(
            request,
            "Venue deleted. Any linked events will remain without a venue.",
        )
        return redirect("venue_list")

    return render(
        request,
        "events/venue_confirm_delete.html",
        {"venue": venue},
    )


# -------------------------
# Resource management
# -------------------------

def resource_list(request):
    resources = Resource.objects.all()

    return render(
        request,
        "events/resource_list.html",
        {"resources": resources},
    )


def resource_create(request):
    if request.method == "POST":
        form = ResourceForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Resource added successfully.",
            )
            return redirect("resource_list")
    else:
        form = ResourceForm()

    return render(
        request,
        "events/resource_form.html",
        {
            "form": form,
            "page_title": "Add Resource",
        },
    )


def resource_update(request, pk):
    resource = get_object_or_404(Resource, pk=pk)

    if request.method == "POST":
        form = ResourceForm(
            request.POST,
            instance=resource,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Resource updated successfully.",
            )
            return redirect("resource_list")
    else:
        form = ResourceForm(instance=resource)

    return render(
        request,
        "events/resource_form.html",
        {
            "form": form,
            "page_title": "Edit Resource",
        },
    )


def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk)

    if request.method == "POST":
        resource.delete()
        messages.success(
            request,
            "Resource deleted successfully.",
        )
        return redirect("resource_list")

    return render(
        request,
        "events/resource_confirm_delete.html",
        {"resource": resource},
    )


def schedule_list(request):
    events = list(
        Event.objects.select_related("venue").order_by(
            "event_date",
            "start_time",
        )
    )

    conflicts = []

    # Compare events that use the same venue on the same date.
    for index, event in enumerate(events):
        if not event.venue_id:
            continue

        for other in events[index + 1:]:
            if other.event_date != event.event_date:
                # Events are ordered by date, so later events
                # will not match this date after it changes.
                if other.event_date > event.event_date:
                    break
                continue

            if other.venue_id != event.venue_id:
                continue

            overlaps = (
                event.start_time < other.end_time
                and event.end_time > other.start_time
            )

            if overlaps:
                conflicts.append({
                    "event_one": event,
                    "event_two": other,
                    "venue": event.venue,
                    "date": event.event_date,
                })

    context = {
        "events": events,
        "conflicts": conflicts,
        "conflict_count": len(conflicts),
    }

    return render(
        request,
        "events/schedule_list.html",
        context,
    )

