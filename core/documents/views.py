from rest_framework import permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import AuthorityIssuedDocument, UserUploadedDocument
from .serializers import AuthorityIssuedDocumentSerializer, UserUploadedDocumentSerializer
from blockchain.services import store_document_on_chain
from blockchain.ipfs_utils import upload_file_to_ipfs
from users.models import CustomUser
from blockchain.models import VerificationHistory

class IssueDocumentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        issuer = request.user
        receiver_id = request.data.get('receiver_id')
        title = request.data.get('title')
        file = request.FILES.get('file')

        if not issuer.is_verified_authority:
            return Response({'error': 'You are not authorized to issue documents.'}, status=403)

        if not receiver_id or not title or not file:
            return Response({'error': 'Missing fields'}, status=400)

        receiver = get_object_or_404(CustomUser, public_id=receiver_id)
        ipfs_hash = upload_file_to_ipfs(file)

        if not ipfs_hash:
            return Response({'error': 'IPFS upload failed'}, status=500)

        tx_hash, document_index, block_tx_hash = store_document_on_chain(
            ipfs_hash,
            issuer.blockchain_address,
            receiver.blockchain_address,
            title,
            issuer.private_key
        )

        doc = AuthorityIssuedDocument.objects.create(
            issuer=issuer,
            receiver=receiver,
            title=title,
            tx_hash=tx_hash,
            ipfs_hash=ipfs_hash,
            document_index=document_index,
            block_tx_hash=block_tx_hash,
        )

        serializer = AuthorityIssuedDocumentSerializer(doc)
        return Response({'status': 'success', 'document': serializer.data}, status=201)


class UserUploadDocumentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        title = request.data.get('title')
        file = request.FILES.get('file')

        if not title or not file:
            return Response({'error': 'Missing fields'}, status=400)

        ipfs_hash = upload_file_to_ipfs(file)

        if not ipfs_hash:
            return Response({'error': 'IPFS upload failed'}, status=500)

        tx_hash, document_index, block_tx_hash = store_document_on_chain(
            ipfs_hash,
            user.blockchain_address,
            user.blockchain_address,
            title,
            user.private_key
        )

        doc = UserUploadedDocument.objects.create(
            owner=user,
            title=title,
            ipfs_hash=ipfs_hash,
            tx_hash=tx_hash,
            document_index=document_index,
            block_tx_hash=block_tx_hash,  # Save block hash here
        )

        serializer = UserUploadedDocumentSerializer(doc)
        return Response({'status': 'success', 'document': serializer.data}, status=201)


class AuthorityUploadedDocumentListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_verified_authority:
            return Response({'error': 'You are not authorized to view this.'}, status=403)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # Return all documents issued by the authority (the logged in user)
        return AuthorityIssuedDocument.objects.filter(issuer=self.request.user)

    serializer_class = AuthorityIssuedDocumentSerializer


class UserDocumentsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # User uploaded documents by the user
        user_docs = UserUploadedDocument.objects.filter(owner=user)
        user_docs_serialized = UserUploadedDocumentSerializer(user_docs, many=True).data

        # Authority issued documents received by the user
        authority_docs = AuthorityIssuedDocument.objects.filter(receiver=user)
        authority_docs_serialized = AuthorityIssuedDocumentSerializer(authority_docs, many=True).data

        # Return both with keys to segregate on frontend
        return Response({
            'user_uploaded_documents': user_docs_serialized,
            'authority_issued_documents': authority_docs_serialized,
        })


class UserDocumentStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Uploaded by user
        user_docs = UserUploadedDocument.objects.filter(owner=user)
        uploaded_docs_count = user_docs.count()

        # Authority issued to user
        authority_docs = AuthorityIssuedDocument.objects.filter(receiver=user)
        authority_docs_count = authority_docs.count()

        # Flagged documents - assuming is_flagged field
        flagged_docs_count = (
            user_docs.filter(flagged=True).count() +
            authority_docs.filter(flagged=True).count()
        )

        return Response({
            'uploaded_documents': uploaded_docs_count,
            'authority_issued_documents': authority_docs_count,
            'flagged_documents': flagged_docs_count,
        })


class AuthorityDashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.is_verified_authority:
            return Response({'error': 'Not authorized'}, status=403)

        issued_docs_count = AuthorityIssuedDocument.objects.filter(issuer=user).count()
        verified_docs_count = VerificationHistory.objects.filter(verifier=user).count()

        return Response({
            'issued_documents_count': issued_docs_count,
            'verified_documents_count': verified_docs_count,
        })