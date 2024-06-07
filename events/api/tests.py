from django.test import TestCase, Client
from django.urls import reverse

from .models import Venue, BoundingBox


class VenueTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_venue_url = reverse("create_venue")


    def test_create_venue_success(self):
        data = {
            "name": "New Venue",
            "capacity": 3000,
            "bounding_box": {
                "min_longitude": 0.715242,
                "max_longitude": 0.715561,
                "min_latitude": 48.639185,
                "max_latitude": 48.639190,
            }
        }
        response = self.client.post(self.create_venue_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Venue.objects.count(), 1)
        self.assertEqual(BoundingBox.objects.count(), 1)
        venue = Venue.objects.first()
        self.assertEqual(venue.name, "New Venue")
        self.assertEqual(venue.capacity, 3000)

    def test_create_venue_missing_name(self):
        data = {
            "capacity": 3000,
            "bounding_box": {
                "min_longitude": 0.715242,
                "max_longitude": 0.715561,
                "min_latitude": 48.639185,
                "max_latitude": 48.639190,
            }
        }
        response = self.client.post(self.create_venue_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
        self.assertEqual(response.json()["error"], "Name is required.")

    def test_create_venue_missing_capacity(self):
        data = {
            "name": "New Venue",
            "bounding_box": {
                "min_longitude": 0.715242,
                "max_longitude": 0.715561,
                "min_latitude": 48.639185,
                "max_latitude": 48.639190,
            }
        }
        response = self.client.post(self.create_venue_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Venue.objects.count(), 1)
        self.assertEqual(BoundingBox.objects.count(), 1)
        venue = Venue.objects.first()
        self.assertEqual(venue.name, "New Venue")
        self.assertIsNone(venue.capacity)

    def test_create_venue_missing_bounding_box(self):
        data = {
            "name": "New Venue",
            "capacity": 3000
        }
        response = self.client.post(self.create_venue_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Venue.objects.count(), 1)
        self.assertEqual(BoundingBox.objects.count(), 0)
        venue = Venue.objects.first()
        self.assertEqual(venue.name, "New Venue")
        self.assertEqual(venue.capacity, 3000)
        self.assertIsNone(venue.bounding_box)