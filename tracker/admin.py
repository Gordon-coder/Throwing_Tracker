from django.contrib import admin

# Register your models here.
from .models import Competitor, Throw, Event


class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'school', 'event')
    list_filter = ('event__gender', 'event__grade', 'event__event_name', 'school')
    search_fields = ('name', 'school', 'number')
    ordering = ('event', 'number')
    list_per_page = 50


class ThrowAdmin(admin.ModelAdmin):
    list_display = ('competitor', 'distance')
    list_filter = ('competitor__event', 'distance')
    search_fields = ('competitor__name',)
    ordering = ('-distance',)
    list_per_page = 50


class EventAdmin(admin.ModelAdmin):
    list_display = ('gender', 'grade', 'event_name')
    list_filter = ('gender', 'grade', 'event_name')
    search_fields = ('event_name',)
    ordering = ('gender', 'grade', 'event_name')
    list_per_page = 50


admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(Throw, ThrowAdmin)
admin.site.register(Event, EventAdmin)