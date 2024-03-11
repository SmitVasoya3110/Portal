from django.contrib import admin
from contact.models import ContactUs, Feedback
# Register your models here.

admin.site.register(ContactUs)

class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ('username', 'email', 'message', 'rating')
    list_display =  ('username', 'email', 'rating')
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(Feedback, FeedbackAdmin)
