from django.contrib import admin
from .models import ValentinePlan, Reaction, LoveLetter


@admin.register(ValentinePlan)
class ValentinePlanAdmin(admin.ModelAdmin):
    list_display = ['your_name', 'partner_name', 'relationship_type', 'city', 'budget', 'plan_type', 'view_count', 'created_at']
    list_filter = ['relationship_type', 'vibe', 'plan_type', 'created_at']
    search_fields = ['your_name', 'partner_name', 'city', 'share_code']
    readonly_fields = ['plan_id', 'share_code', 'created_at', 'view_count']
    
    fieldsets = (
        ('Plan Information', {
            'fields': ('plan_id', 'share_code', 'created_at', 'view_count')
        }),
        ('User Details', {
            'fields': ('your_name', 'partner_name', 'relationship_type', 'city', 'budget', 'plan_type', 'vibe')
        }),
        ('Generated Content', {
            'fields': ('plan_content',)
        }),
        ('Metadata', {
            'fields': ('is_anonymous', 'creator_ip')
        }),
    )


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['plan', 'reaction_type', 'created_at']
    list_filter = ['reaction_type', 'created_at']
    readonly_fields = ['created_at']


@admin.register(LoveLetter)
class LoveLetterAdmin(admin.ModelAdmin):
    list_display = ['your_name', 'partner_name', 'created_at']
    search_fields = ['your_name', 'partner_name']
    readonly_fields = ['created_at']
