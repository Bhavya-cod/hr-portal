from django.db import models
from django.conf import settings

class EmployeeProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    responsibilities = models.TextField(blank=True, null=True, help_text="What this employee does daily")
    remarks = models.TextField(blank=True, null=True, help_text="HR or CEO notes about this employee")
    date_joined = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Profile: {self.user.username}"

class EmployeeTask(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.employee.username}"

class EmployeeDocument(models.Model):
    DOCUMENT_TYPES = [
        ('10th', '10th Certificate'),
        ('12th', '12th/Intermediate'),
        ('diploma', 'Diploma'),
        ('degree', 'Bachelor Degree'),
        ('pg', 'Master/Post Graduation'),
        ('other', 'Other Document')
    ]
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='employee_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.employee.username}"

class PerformanceFeedback(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_received')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_given')
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5, help_text="Rating from 1 to 5")
    is_self_evaluation = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        type_str = "Self" if self.is_self_evaluation else "HR"
        return f"{type_str} Feedback: {self.employee.username} ({self.created_at.date()})"
