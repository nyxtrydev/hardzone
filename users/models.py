from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Super Admin'),
        ('MANAGER', 'Manager'),
        ('EMPLOYEE', 'Employee'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')
    department = models.ForeignKey('budgets.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    status = models.BooleanField(default=True) # True for Active, False for Inactive

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
