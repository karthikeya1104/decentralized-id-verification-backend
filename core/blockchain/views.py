from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from blockchain.services import set_document_flag, verify_document_by_tx_hash, verify_document_by_index
from .models import VerificationHistory, FlagHistory
from users.models import CustomUser
from rest_framework.exceptions import ValidationError
from documents.models import AuthorityIssuedDocument, UserUploadedDocument

class FlagDocumentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        index = request.data.get("index")
        flag = request.data.get("flag")

        if index is None or flag is None:
            return Response({'error': 'Missing fields'}, status=400)

        try:
            index = int(index)
            flag = str(flag).lower() == 'true'
        except ValueError:
            return Response({'error': 'Invalid index or flag value'}, status=400)

        user = request.user

        try:
            # Update on-chain
            set_document_flag(index, user.blockchain_address, user.private_key, flag)

            # Save history
            FlagHistory.objects.create(
                document_index=index,
                actor=user,
                flag_status=flag
            )

            # Try updating AuthorityIssuedDocument
            updated = False

            doc = AuthorityIssuedDocument.objects.filter(document_index=index).first()
            if doc:
                doc.flagged = flag
                doc.save()
                updated = True
            else:
                doc = UserUploadedDocument.objects.filter(document_index=index).first()
                if doc:
                    doc.flagged = flag
                    doc.save()
                    updated = True

            if not updated:
                return Response({"warning": "Flag set on-chain, but no matching local document found."}, status=202)

        except Exception as e:
            return Response({'error': str(e)}, status=500)

        return Response({"message": "Flag status updated."}, status=200)


class VerifyDocumentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        index = request.data.get("index")
        tx_hash = request.data.get("tx_hash")
        
        if user.role != 'authority' or not user.is_verified_authority:
            return Response({"error": "Only authority users can verify documents."}, status=403)
        
        if index is None and tx_hash is None:
            raise ValidationError({"detail": "Either 'index' or 'tx_hash' must be provided."})
        
        try:
            if index is not None:
                index = int(index)
                # Call verifyByIndex contract wrapper
                result = verify_document_by_index(index)
                exists = result[0]
                
                response_data = {
                    "exists": exists,
                    "ipfsHash": result[1],
                    "issuer": result[2],
                    "receiver": result[3],
                    "title": result[4],
                    "timestamp": result[5],
                    "flagged": result[6],
                    "block_hash": result[7],
                }
                document_index = index

            else:
                # Call verifyByTxHash contract wrapper
                tx_hash = "0x" + tx_hash
                result = verify_document_by_tx_hash(tx_hash)
                exists = result[0]

                response_data = {
                    "exists": exists,
                    "index": result[1],
                    "ipfsHash": result[2],
                    "issuer": result[3],
                    "receiver": result[4],
                    "title": result[5],
                    "timestamp": result[6],
                    "flagged": result[7],
                    # No txHash here, tx_hash is input
                    "block_hash": tx_hash,
                }
                document_index = result[1]

            verified_user = None
            if exists:
                try:
                    verified_user = CustomUser.objects.get(blockchain_address=response_data["receiver"])
                except CustomUser.DoesNotExist:
                    pass

            VerificationHistory.objects.create(
                verifier=user,
                verified_user=verified_user,
                document_index=document_index,
                success=exists,
                response_data=response_data if exists else {},
            )

            if not exists:
                return Response({"exists": False}, status=200)

            return Response(response_data, status=200)

        except Exception as e:
            VerificationHistory.objects.create(
                verifier=user,
                document_index=index if index is not None else None,
                success=False,
                response_data={"error": str(e)},
            )
            return Response({"error": str(e)}, status=500)
