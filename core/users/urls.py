from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AuthorityRegisterView, CustomTokenObtainPairView, SystemStatsView

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('authority/register/', AuthorityRegisterView.as_view(), name='authority_register'),
    path('stats/', SystemStatsView.as_view(), name='system-stats'),
]
