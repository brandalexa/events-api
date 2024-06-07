from django.urls import path
from .views import create_venue, get_venue, get_artists_at_event

urlpatterns = [
    path("venues/", create_venue, name="create_venue"),
    path("venues/<int:venue_id>/", get_venue, name="get_venue"),
    path("events/<int:event_id>/artists/", get_artists_at_event, name="get_artists_at_event"),
]