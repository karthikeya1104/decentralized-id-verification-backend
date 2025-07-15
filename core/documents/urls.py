from django.urls import path
from .views import IssueDocumentView, UserUploadDocumentView, UserDocumentsListView, AuthorityUploadedDocumentListView, UserDocumentStatsView, AuthorityDashboardStatsView

urlpatterns = [
    path('issue/', IssueDocumentView.as_view(), name='issue-document'),
    path('upload/', UserUploadDocumentView.as_view(), name='user-upload-document'),
    path('user-documents/', UserDocumentsListView.as_view(), name='user-documents-list'),
    path('authority-documents/', AuthorityUploadedDocumentListView.as_view(), name='authority-documents-list'),
    path('user/document-stats/', UserDocumentStatsView.as_view(), name='user-document-stats'),
    path('authority/document-stats/', AuthorityDashboardStatsView.as_view(), name='authority-dashboard-stats')
]


"""
flag/ 
{
  "index": 3,
  "flag": true
}
"""