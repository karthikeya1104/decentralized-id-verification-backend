from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/blockchain/', include('blockchain.urls')),
]
