from django.db import models
from django.conf import settings

class VerificationHistory(models.Model):
    verifier = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='verifications_made'
    )
    verified_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='verifications_received', null=True, blank=True
    )
    tx_hash = models.CharField(max_length=100, null=True, blank=True)
    ipfs_hash = models.CharField(max_length=255, null=True, blank=True)
    document_index = models.IntegerField(null=True, blank=True)
    verified_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()
    response_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Verification by {self.verifier} on {self.verified_user} at {self.verified_at} - Success: {self.success}"


class FlagHistory(models.Model):
    FLAG_STATUS_CHOICES = (
        (True, 'Flagged'),
        (False, 'Unflagged'),
    )

    document_index = models.PositiveIntegerField()
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='flag_actions')
    flag_status = models.BooleanField(choices=FLAG_STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.document_index} flagged={self.flag_status} by {self.actor}"
