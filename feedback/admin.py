from django.contrib import admin
from django.utils.html import format_html

from .models import Feedback

# Only allow viewing of feedback
class FeedbackAdmin(admin.ModelAdmin):
    fields = ['created_at', 'admin_language', ('download', 'recording')]
    list_display = ['created_at', 'admin_language', 'recording']

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
    
    @admin.display(description='Download')
    def download(self, obj):
        return format_html('<a href="{}" download>{}</a>', obj.recording_file.url, obj.recording_file.name)

    # Make the language a bit more readable
    @admin.display(description='Language')
    def admin_language(self, obj):
        return {
            'en': 'English',
            'fr': 'French',
        }.get(obj.language, 'Unknown')
    admin_language.admin_order_field = 'language'
    
    def recording(self, obj):
        return format_html('<audio controls><source src="{}" type="audio/wav"></audio>', obj.recording_file.url)


admin.site.register(Feedback, FeedbackAdmin)
