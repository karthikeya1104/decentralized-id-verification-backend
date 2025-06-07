from django.urls import path
from .views import FlagDocumentView, VerifyDocumentView

urlpatterns = [
    path('flag/', FlagDocumentView.as_view(), name='flag-document'),
    path('verify/', VerifyDocumentView.as_view(), name='verify-document'),
]