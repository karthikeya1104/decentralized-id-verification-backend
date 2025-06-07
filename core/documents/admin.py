from django.contrib import admin
from .models import AuthorityIssuedDocument, UserUploadedDocument

@admin.register(AuthorityIssuedDocument)
class AuthorityIssuedDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_index', 'issuer', 'receiver', 'issued_at', 'tx_hash', 'ipfs_hash', 'block_tx_hash', 'flagged')
    search_fields = ('title', 'issuer__username', 'receiver__username', 'tx_hash', 'ipfs_hash')
    list_filter = ('issued_at',)

@admin.register(UserUploadedDocument)
class UserUploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_index', 'owner', 'uploaded_at', 'tx_hash', 'ipfs_hash', 'block_tx_hash', 'flagged')
    search_fields = ('title', 'owner__username', 'tx_hash', 'ipfs_hash')
    list_filter = ('uploaded_at',)