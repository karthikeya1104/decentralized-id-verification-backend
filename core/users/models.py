from django.contrib.auth.models import AbstractUser
from django.db import models
from eth_account import Account
import uuid

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('authority', 'Authority'),
    ]

    public_id = models.CharField(max_length=100, unique=True, blank=True)
    blockchain_address = models.CharField(max_length=42, blank=True, null=True)
    private_key = models.CharField(max_length=128, blank=True, null=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    # Authority-only fields
    name = models.CharField(max_length=100, blank=True)
    sector = models.CharField(max_length=100, blank=True)
    proof_document = models.FileField(upload_to='user_proofs/', null=True, blank=True)
    is_verified_authority = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = str(uuid.uuid4())
        if not self.blockchain_address or not self.private_key:
            acct = Account.create()
            self.blockchain_address = acct.address
            self.private_key = acct.key.hex()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username if self.username else self.public_id} ({self.role})"
