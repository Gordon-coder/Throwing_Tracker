from django.contrib import admin
from .models import Event, Competitor, Throw

# Register your models here.
admin.site.register(Event)
admin.site.register(Competitor)
admin.site.register(Throw)
