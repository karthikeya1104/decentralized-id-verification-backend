from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SystemLog(models.Model):
    LEVEL_CHOICES = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
    ]
    
    EVENT_CHOICES = [
        ('LOGIN', 'Login'),
        ('REGISTER', 'Register'),
        ('UPLOAD_DOCUMENT', 'Upload Document'),
        ('ISSUE_DOCUMENT', 'Issue Document'),
        ('VERIFY_AUTHORITY', 'Verify Authority'),
        ('FLAG_DOCUMENT', 'Flag Document'),
        ('CREATE_USER', 'create user'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES, default='OTHER')
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField(null=True, blank=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.level} - {self.path} - {self.created_at}"
