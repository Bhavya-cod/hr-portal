from django.contrib import admin
from .models import Announcement, CompanyPolicy, CalendarEvent

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'priority', 'is_active')
    list_filter = ('priority', 'is_active', 'date_posted')
    search_fields = ('title', 'content')

@admin.register(CompanyPolicy)
class CompanyPolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'last_updated')
    search_fields = ('title', 'description')

@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'event_type')
    list_filter = ('event_type', 'start_date')
    search_fields = ('name', 'description')
