import json

from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import BoundingBox, Venue, Event


@csrf_exempt
def create_venue(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            name = data.get("name")
            if name is None:
                return JsonResponse({"error": "Name is required."}, status=400)

            venue = Venue(name=name)

            bounding_box_data = data.get('bounding_box')
            if bounding_box_data is not None:
                min_longitude = bounding_box_data.get('min_longitude')
                max_longitude = bounding_box_data.get('max_longitude')
                min_latitude = bounding_box_data.get('min_latitude')
                max_latitude = bounding_box_data.get('max_latitude')

                if not min_longitude or not max_longitude or not min_latitude or not max_latitude:
                    return JsonResponse({
                        "error": "Bounding box must contain min and max latitude and longitude."
                    }, status=400)

                bounding_box = BoundingBox(
                    min_longitude=min_longitude,
                    max_longitude=max_longitude,
                    min_latitude=min_latitude,
                    max_latitude=max_latitude
                )

                bounding_box.full_clean()
                bounding_box.save()

                venue.bounding_box = bounding_box

            capacity = data.get('capacity')
            if capacity is not None:
                venue.capacity = capacity

            venue.clean()
            venue.save()

            return JsonResponse(venue.to_dict(), status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed."}, status=405)


@csrf_exempt
def get_venue(request, venue_id):
    if request.method == "GET":
        try:
            venue = Venue.objects.get(id=venue_id)
            return JsonResponse(venue.to_dict())

        except Venue.DoesNotExist:
            return JsonResponse({"error": "Requested venue not found."}, status=404)
    return JsonResponse({"error": "Method not allowed."}, status=405)


@csrf_exempt
def get_artists_at_event(request, event_id):
    if request.method == "GET":
        try:
            event = Event.objects.get(id=event_id)
            artists = event.artists.all()
            artists_response = [artist.to_dict() for artist in artists]
            return JsonResponse({"artists": artists_response})

        except Event.DoesNotExist:
            return JsonResponse({"error": "Requested event not found."}, status=404)
    return JsonResponse({"error": "Method not allowed."}, status=405)