from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import (
    StaffLoginSerializer,
    UserSummarySerializer,
    AuthoritySummarySerializer,
    AuthorityVerificationSerializer,
    StaffCreateUserSerializer,
    SystemLogSerializer,
    VerificationHistorySerializer,
    FlagHistorySerializer
)
from users.models import CustomUser
from core.utils import log_event
from core.models import SystemLog
from blockchain.models import VerificationHistory, FlagHistory

# ----------------------
# Staff Login View
# ----------------------
class StaffLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = StaffLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# ----------------------
# All Users and Authorities View
# ----------------------
class AllUsersAuthoritiesView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        users_qs = CustomUser.objects.filter(role='user')
        authorities_qs = CustomUser.objects.filter(role='authority')

        users_data = UserSummarySerializer(users_qs, many=True, context={"request": request}).data
        authorities_data = AuthoritySummarySerializer(authorities_qs, many=True, context={"request": request}).data

        return Response({
            "users": users_data,
            "authorities": authorities_data
        })


# ----------------------
# Verify/Unverify Authority View
# ----------------------
class AuthorityVerifyView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = AuthorityVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        authority_id = serializer.validated_data['authority_id']
        verify = serializer.validated_data['verify']

        authority = CustomUser.objects.get(id=authority_id, role='authority')

        if not authority.proof_document:
            return Response(
                {"error": "Authority has no proof document uploaded."},
                status=status.HTTP_400_BAD_REQUEST
            )

        authority.is_verified_authority = verify
        authority.save()

        status_msg = "verified" if verify else "unverified"

        proof_doc_url = None
        if authority.proof_document:
            proof_doc_url = request.build_absolute_uri(authority.proof_document.url)
               
        log_event(
            user=request.user,
            event_type="VERIFY_AUTHORITY",
            level="INFO",
            message=f"Authority {authority.username} has been {status_msg}",
            path=request.path,
            method=request.method,
            status_code=200
        )

        return Response({
            "message": f"Authority {authority.name} has been {status_msg} successfully.",
            "authority": {
                "id": authority.id,
                "name": authority.name,
                "is_verified_authority": authority.is_verified_authority,
                "proof_document": proof_doc_url,
                "sector": authority.sector
            }
        }, status=status.HTTP_200_OK)

class CreateUserAPI(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        username = request.data.get("username")
        public_id = request.data.get("public_id")

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if public_id is provided and already exists
        if public_id and CustomUser.objects.filter(public_id=public_id).exists():
            return Response(
                {"error": "Public ID already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StaffCreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            log_event(
                user=request.user,
                event_type="CREATE_USER",
                level="INFO",
                message=f"User '{user.username}' created successfully",
                path=request.path,
                method=request.method,
                status_code=201
            )
            
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

        # If serializer fails for some other reason
        
        log_event(
            user=request.user,
            level="ERROR",
            message=f"Failed to create user. Errors: {serializer.errors}",
            path=request.path,
            method=request.method,
            status_code=400
        )
        
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SystemLogsView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Only admin access

    def get(self, request):
        # Optional: limit number of logs to latest 100 for performance
        system_logs = SystemLog.objects.order_by('-created_at')[:100]
        verification_logs = VerificationHistory.objects.order_by('-verified_at')[:100]
        flag_logs = FlagHistory.objects.order_by('-timestamp')[:100]

        system_logs_serialized = SystemLogSerializer(system_logs, many=True).data
        verification_logs_serialized = VerificationHistorySerializer(verification_logs, many=True).data
        flag_logs_serialized = FlagHistorySerializer(flag_logs, many=True).data
        
        return Response({
            "system_logs": system_logs_serialized,
            "verification_history": verification_logs_serialized,
            "flag_history": flag_logs_serialized
        })