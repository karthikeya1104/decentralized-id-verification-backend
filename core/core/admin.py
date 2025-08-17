from django.contrib import admin
from .models import SystemLog

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'event_type', 'level', 'path', 'method', 'status_code', 'user']
    list_filter = ['level', 'created_at', 'event_type']
    search_fields = ['path', 'message']
