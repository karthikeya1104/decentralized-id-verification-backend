from django.urls import path
from .views import IssueDocumentView, UserUploadDocumentView, UserDocumentsListView, AuthorityUploadedDocumentListView

urlpatterns = [
    path('issue/', IssueDocumentView.as_view(), name='issue-document'),
    path('upload/', UserUploadDocumentView.as_view(), name='user-upload-document'),
    path('user-documents/', UserDocumentsListView.as_view(), name='user-documents-list'),
    path('authority-documents/', AuthorityUploadedDocumentListView.as_view(), name='authority-documents-list'),
]


"""
flag/ 
{
  "index": 3,
  "flag": true
}
"""