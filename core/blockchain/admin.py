from django.contrib import admin
from .models import FlagHistory, VerificationHistory


@admin.register(FlagHistory)
class FlagHistoryAdmin(admin.ModelAdmin):
    list_display = ('document_index', 'actor', 'flag_status', 'timestamp')
    list_filter = ('flag_status', 'timestamp')
    search_fields = ('actor__username', 'document_index')


@admin.register(VerificationHistory)
class VerificationHistoryAdmin(admin.ModelAdmin):
    list_display = ('verifier', 'verified_user', 'success', 'document_index', 'verified_at')
    list_filter = ('success', 'verified_at')
    search_fields = ('verifier__username', 'verified_user__username', 'document_index')
