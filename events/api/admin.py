from django.contrib import admin
from .models import *

admin.site.register(Event)
admin.site.register(Artist)
admin.site.register(Venue)
admin.site.register(BoundingBox)
