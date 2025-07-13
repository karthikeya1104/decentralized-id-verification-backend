from rest_framework import serializers
from .models import AuthorityIssuedDocument, UserUploadedDocument


class UserUploadedDocumentSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    owner_public_id = serializers.CharField(source='owner.public_id', read_only=True)

    class Meta:
        model = UserUploadedDocument
        fields = [
            'id',
            'owner',
            'owner_name',
            'owner_public_id',
            'title',
            'ipfs_hash',
            'tx_hash',
            'block_tx_hash',       
            'document_index',
            'uploaded_at',
            'flagged',
        ]
        read_only_fields = ['ipfs_hash', 'tx_hash', 'block_tx_hash', 'document_index', 'uploaded_at']


class AuthorityIssuedDocumentSerializer(serializers.ModelSerializer):
    issuer_name = serializers.CharField(source='issuer.name', read_only=True)
    issuer_public_id = serializers.CharField(source='issuer.public_id', read_only=True)
    receiver_name = serializers.CharField(source='receiver.username', read_only=True)
    receiver_public_id = serializers.CharField(source='receiver.public_id', read_only=True)

    class Meta:
        model = AuthorityIssuedDocument
        fields = [
            'id',
            'issuer',
            'issuer_name',
            'issuer_public_id',
            'receiver',
            'receiver_name',
            'receiver_public_id',
            'title',
            'ipfs_hash',
            'tx_hash',
            'block_tx_hash',   
            'document_index',
            'issued_at',
            'flagged',
        ]
        read_only_fields = ['ipfs_hash', 'tx_hash', 'block_hash', 'document_index', 'issued_at']
