from django.db import models
from django.conf import settings
from django.utils import timezone

class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=timezone.now)
    
    morning_check_in = models.DateTimeField(null=True, blank=True)
    morning_location = models.CharField(max_length=100, null=True, blank=True)
    
    lunch_check_out = models.DateTimeField(null=True, blank=True)
    lunch_location = models.CharField(max_length=100, null=True, blank=True)
    
    afternoon_check_in = models.DateTimeField(null=True, blank=True)
    afternoon_location = models.CharField(max_length=100, null=True, blank=True)
    
    final_check_out = models.DateTimeField(null=True, blank=True)
    final_location = models.CharField(max_length=100, null=True, blank=True)
    
    ATTENDANCE_STATUS = [
        ('Normal', 'Normal'),
        ('LOP', 'Loss of Pay'),
    ]
    status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS, default='Normal')
    
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    @property
    def next_action(self):
        if not self.morning_check_in:
            return 'morning_check_in'
        if not self.lunch_check_out:
            return 'lunch_check_out'
        if not self.afternoon_check_in:
            return 'afternoon_check_in'
        if not self.final_check_out:
            return 'final_check_out'
        return None

    @property
    def total_working_hours(self):
        if self.morning_check_in and self.final_check_out:
            delta = self.final_check_out - self.morning_check_in
            return delta.total_seconds() / 3600.0
        elif self.morning_check_in:
            # If today, calculate up to now
            if self.date == timezone.now().date():
                delta = timezone.now() - self.morning_check_in
                return delta.total_seconds() / 3600.0
        return 0.0

class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('Paid', 'Paid Leave'),
        ('LOP', 'Loss of Pay'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leave_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPES, default='Paid')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    admin_remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.start_date} to {self.end_date} ({self.leave_type})"
