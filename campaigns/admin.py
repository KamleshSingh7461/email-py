from django.contrib import admin
from .models import Campaign, CampaignLog

class CampaignLogInline(admin.TabularInline):
    model = CampaignLog
    extra = 0
    readonly_fields = ('contact', 'sent_at', 'status', 'error_message')

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'created_by')
    search_fields = ('name',)
    inlines = [CampaignLogInline]

@admin.register(CampaignLog)
class CampaignLogAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'contact', 'status', 'sent_at')
    list_filter = ('status', 'campaign')
