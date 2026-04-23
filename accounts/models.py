from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        CEO = 'CEO', 'CEO'
        HR = 'HR', 'HR'
        FEMALE_HR = 'FEMALE_HR', 'Female HR'
        EMPLOYEE = 'EMPLOYEE', 'Employee'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE
    )

    def is_admin(self):
        return self.role in [self.Role.CEO, self.Role.HR, self.Role.FEMALE_HR] or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
