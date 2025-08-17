from django.urls import path
from .views import StaffLoginView, AllUsersAuthoritiesView, AuthorityVerifyView, CreateUserAPI, SystemLogsView

urlpatterns = [
    path('login/', StaffLoginView.as_view(), name='staff-login'),
    path('all-users/', AllUsersAuthoritiesView.as_view(), name='all-users-authorities'),
    path('verify-authority/', AuthorityVerifyView.as_view(), name='verify-authority'),
    path('create-user/', CreateUserAPI.as_view(), name='create_user_api'),
    path('system-logs/', SystemLogsView.as_view(), name='system-logs'),
]
