from django.db import models
from django.conf import settings

class AuthorityIssuedDocument(models.Model):
    issuer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issued_documents')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_documents')
    title = models.CharField(max_length=255)
    issued_at = models.DateTimeField(auto_now_add=True)
    tx_hash = models.CharField(max_length=66) 
    ipfs_hash = models.CharField(max_length=255)
    document_index = models.PositiveIntegerField(null=True, blank=True)
    block_tx_hash = models.CharField(max_length=66, null=True, blank=True)
    flagged = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} -> {self.receiver.public_id}"


class UserUploadedDocument(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_documents')
    title = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tx_hash = models.CharField(max_length=66, blank=True, null=True)
    ipfs_hash = models.CharField(max_length=255, blank=True, null=True)
    document_index = models.PositiveIntegerField(null=True, blank=True)
    block_tx_hash = models.CharField(max_length=66, null=True, blank=True)
    flagged = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} ({self.owner.public_id})"
