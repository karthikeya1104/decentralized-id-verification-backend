from rest_framework import generics, permissions
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import AuthorityRegistrationSerializer
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from documents.models import AuthorityIssuedDocument
from blockchain.models import VerificationHistory

class AuthorityRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AuthorityRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SystemStatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        documents_issued = AuthorityIssuedDocument.objects.count()
        documents_verified = VerificationHistory.objects.filter(success=True).count()
        authorities_registered = CustomUser.objects.filter(is_verified_authority=True).count()
        
        return Response({
            "documents_issued": documents_issued,
            "documents_verified": documents_verified,
            "authorities_registered": authorities_registered
        })
