from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        # Add custom claims
        token['role'] = user.role
        return token

class AuthorityRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['public_id', 'password', 'username', 'name', 'sector', 'proof_document']
    
    def create(self, validated_data):
        print(validated_data)
        validated_data['role'] = 'authority'
        validated_data['is_verified_authority'] = False
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomTokenObtainPairSerializer(serializers.Serializer):
    public_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        public_id = attrs.get('public_id')
        password = attrs.get('password')
        
        try:
            user = CustomUser.objects.get(public_id=public_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid Password')

        refresh = CustomUserToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'name': user.username,
                'role': user.role,
            }
        }
