
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event,Venue,Resource
from .forms import EventForm,VenueForm,ResourceForm
from datetime import date
from django.contrib import messages


def event_list(request):
    events = Event.objects.all()

    return render(
        request,
        "events/event_list.html",
        {"events": events},
    )


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

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
        return redirect("event_list")

    return render(
        request,
        "events/event_confirm_delete.html",
        {"event": event},
    )


def dashboard(request):
    events = Event.objects.all()
    today = date.today()

    edit_id = request.GET.get("edit")
    edit_event = None

    if edit_id:
        edit_event = get_object_or_404(Event, pk=edit_id)
    else:
        edit_event = events.first()

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
            edit_form = EventForm(
                request.POST,
                instance=edit_event,
            )

            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, "Event updated successfully.")
                return redirect(
                    f"/?edit={edit_event.pk}"
                )

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
        "available_venues": 0,
        "total_resources": Resource.objects.count(),
        "create_form": create_form,
        "edit_form": edit_form,
        "edit_event": edit_event,
    }

    return render(request, "events/dashboard.html", context)
