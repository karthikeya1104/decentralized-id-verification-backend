from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from documents.models import AuthorityIssuedDocument, UserUploadedDocument
from blockchain.models import VerificationHistory, FlagHistory
from core.models import SystemLog

# ----------------------
# Staff Login Serializer
# ----------------------
class StaffLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_staff:
            raise serializers.ValidationError("You are not authorized as staff")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "username": user.username,
                "role": "staff" if user.is_staff else "user",
            },
        }


# ----------------------
# User Summary Serializer
# ----------------------
class UserSummarySerializer(serializers.ModelSerializer):
    uploaded_docs_count = serializers.SerializerMethodField()
    issued_docs_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'public_id', 'uploaded_docs_count', 'issued_docs_count']

    def get_uploaded_docs_count(self, obj):
        # Count from UserUploadedDocument model
        return UserUploadedDocument.objects.filter(owner=obj).count()

    def get_issued_docs_count(self, obj):
        # Count from AuthorityIssuedDocument model
        return AuthorityIssuedDocument.objects.filter(receiver=obj).count()


# ----------------------
# Authority Summary Serializer
# ----------------------
class AuthoritySummarySerializer(serializers.ModelSerializer):
    docs_issued = serializers.SerializerMethodField()
    docs_verified = serializers.SerializerMethodField()
    proof_document = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'public_id', 'name', 'is_verified_authority', 'proof_document', 'sector', 'docs_issued', 'docs_verified']

    def get_docs_issued(self, obj):
        # Count documents issued by this authority
        return AuthorityIssuedDocument.objects.filter(issuer=obj).count()

    def get_docs_verified(self, obj):
        # Count verifications done by this authority
        return VerificationHistory.objects.filter(verifier=obj, success=True).count()
    
    def get_proof_document(self, obj):
        request = self.context.get("request")
        if obj.proof_document and request:
            return request.build_absolute_uri(obj.proof_document.url)
        elif obj.proof_document:
            # fallback if request not in context
            return obj.proof_document.url
        return None


# ----------------------
# Authority Verification Serializer
# ----------------------
class AuthorityVerificationSerializer(serializers.Serializer):
    authority_id = serializers.IntegerField()
    verify = serializers.BooleanField()

    def validate_authority_id(self, value):
        try:
            user = CustomUser.objects.get(id=value, role='authority')
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Authority not found")
        return value


class StaffCreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'public_id', 'password']

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            public_id=validated_data.get('public_id')
        )
        user.set_password(validated_data['password'])
        user.role = 'user'  # force role
        user.save()
        return user


class SystemLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Shows username or None

    class Meta:
        model = SystemLog
        fields = '__all__'


class VerificationHistorySerializer(serializers.ModelSerializer):
    verifier = serializers.StringRelatedField()
    verified_user = serializers.StringRelatedField()

    class Meta:
        model = VerificationHistory
        fields = '__all__'


class FlagHistorySerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()

    class Meta:
        model = FlagHistory
        fields = '__all__'