
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),

    # Events
    path("events/", views.event_list, name="event_list"),
    path("events/create/", views.event_create, name="event_create"),
    path("events/<int:pk>/", views.event_detail, name="event_detail"),
    path("events/<int:pk>/edit/", views.event_update, name="event_update"),
    path("events/<int:pk>/delete/", views.event_delete, name="event_delete"),

    # Venues
    path("venues/", views.venue_list, name="venue_list"),
    path("venues/create/", views.venue_create, name="venue_create"),
    path("venues/<int:pk>/edit/", views.venue_update, name="venue_update"),
    path("venues/<int:pk>/delete/", views.venue_delete, name="venue_delete"),

    
path("resources/", views.resource_list, name="resource_list"),
path("resources/create/", views.resource_create, name="resource_create"),
path("resources/<int:pk>/edit/", views.resource_update, name="resource_update"),
path("resources/<int:pk>/delete/", views.resource_delete, name="resource_delete"),
path("schedule/", views.schedule_list, name="schedule_list"),
]
