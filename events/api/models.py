from django.core.exceptions import ValidationError
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            key: value for key, value in {
                "id": self.id,
                "name": self.name,
                "capacity": self.genre,
            }.items() if value is not None
        }


class BoundingBox(models.Model):
    min_longitude = models.FloatField()
    max_longitude = models.FloatField()
    min_latitude = models.FloatField()
    max_latitude = models.FloatField()

    def clean(self):
        if self.min_longitude >= self.max_longitude:
            raise ValidationError("min_longitude must be less than max_longitude.")
        if self.min_latitude >= self.max_latitude:
            raise ValidationError("min_latitude must be less than max_latitude.")

    def __str__(self):
        return f"BoundingBox(({self.min_latitude}, {self.min_longitude}), ({self.max_latitude}, {self.max_longitude}))"




class Venue(models.Model):
    name = models.CharField(max_length=255)
    bounding_box = models.OneToOneField(BoundingBox, on_delete=models.CASCADE, blank=True, null=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.bounding_box is not None:
            self.bounding_box.clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def to_dict(self):
        return {
            key: value for key, value in {
                "id": self.id,
                "name": self.name,
                "bounding_box": {
                    "id": self.bounding_box.id,
                    "min_latitude": self.bounding_box.min_latitude,
                    "max_latitude": self.bounding_box.max_latitude,
                    "min_longitude": self.bounding_box.min_longitude,
                    "max_longitude": self.bounding_box.max_longitude,
                } if self.bounding_box is not None else None,
                "capacity": self.capacity,
            }.items() if value is not None
        }


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="events")
    artists = models.ManyToManyField(Artist, blank=True, related_name="events")

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            key: value for key, value in {
                "id": self.id,
                "name": self.name,
                "date": self.date if self.date is not None else None,
                "venue": self.venue.to_dict() if self.venue is not None else None,
                "artists": [artist.to_dict() for artist in self.artists.all()],
            }.items() if value is not None
        }