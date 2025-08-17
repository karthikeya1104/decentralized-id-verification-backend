from rest_framework import generics, permissions
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import AuthorityRegistrationSerializer
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from documents.models import AuthorityIssuedDocument
from blockchain.models import VerificationHistory
from core.utils import log_event

class AuthorityRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AuthorityRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Log the registration event
        log_event(
            user=user,
            event_type="REGISTER",
            level="INFO",
            message=f"New authority registered: {user.username}",
            path=self.request.path,
            method=self.request.method,
            status_code=201
        )

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Log login attempts only if successful
        if response.status_code == 200:
            user = CustomUser.objects.filter(username=request.data.get("username")).first()
            log_event(
                user=user,
                event_type="LOGIN",
                level="INFO",
                message=f"User logged in: {user.username}" if user else "Unknown user login attempt",
                path=request.path,
                method=request.method,
                status_code=response.status_code
            )
        return response


class SystemStatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        documents_issued = AuthorityIssuedDocument.objects.count()
        documents_verified = VerificationHistory.objects.filter(success=True).count()
        authorities_registered = CustomUser.objects.filter(role="authority").count()
        
        return Response({
            "documents_issued": documents_issued,
            "documents_verified": documents_verified,
            "authorities_registered": authorities_registered
        })
