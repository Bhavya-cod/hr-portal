from django.db import models
from django.utils import timezone

class Announcement(models.Model):
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        NORMAL = 'NORMAL', 'Normal'
        HIGH = 'HIGH', 'High'
        URGENT = 'URGENT', 'Urgent'

    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.NORMAL)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class CompanyPolicy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    last_updated = models.DateField(auto_now=True)
    file_attachment = models.FileField(upload_to='policies/', blank=True, null=True, help_text="Upload a PDF of the policy if applicable")

    class Meta:
        verbose_name_plural = "Company Policies"

    def __str__(self):
        return self.title

class CalendarEvent(models.Model):
    class EventType(models.TextChoices):
        HOLIDAY = 'HOLIDAY', 'Holiday'
        MEETING = 'MEETING', 'Company Meeting'
        DEADLINE = 'DEADLINE', 'Important Deadline'
        OTHER = 'OTHER', 'Other'

    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if it's a single day event")
    event_type = models.CharField(max_length=20, choices=EventType.choices, default=EventType.OTHER)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
