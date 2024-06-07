import sys

from .models import Artist, Venue, Event, BoundingBox


def create_sample_data():

    if "test" in sys.argv:
        return

    if Artist.objects.count() > 0 or Venue.objects.count() > 0 or Event.objects.count() > 0:
        return

    artist1 = Artist.objects.create(name="Dua Lipa", genre="Pop")
    artist2 = Artist.objects.create(name="Bob Marley", genre="Reggae")

    bounding_box = BoundingBox.objects.create(
        min_longitude=-0.243683,
        max_longitude=-0.243673,
        min_latitude=51.052235,
        max_latitude=51.052245
    )

    venue = Venue.objects.create(
        name="Glastonbury",
        capacity=5000,
        bounding_box=bounding_box
    )

    event = Event.objects.create(
        name="Rave",
        date="2024-06-06",
        venue=venue
    )

    event.artists.set([artist1, artist2])
