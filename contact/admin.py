import time
from django.contrib import admin
from contact.forms import AdminReplyForm
from contact.models import AdminReply, ContactUs, Feedback
from django.core.mail import send_mail
from django.conf import settings 
# Register your models here.

class AdminReplyInline(admin.StackedInline):
    model = AdminReply
    form = AdminReplyForm
    extra = 1

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'replied')
    list_filter = ('replied',)
    inlines = [AdminReplyInline]

    # def save_model(self, request, obj, form, change):
    #     print(request)
    #     print(obj.adminreply_set)
    #     # Override the save_model method to set replied to True
    #     obj.replied = True
    #     obj.save()
    def save_related(self, request:list, form, formsets, change):
        print(form)
        message = form.cleaned_data.get('message')
        email_id = form.cleaned_data.get('email')
        for formset in formsets:
            # Found this simple way to check dynamic class instance.
            if formset.model == AdminReply:
                instances = formset.save(commit=False)
                print(instances)
                for instance in instances:
                    instance.admin_user = request.user
                    instance.save()

                    subject = 'Reply: Contact Us'
                    html_message = f"""<p>{message}</p> 
                                    <hr>
                                    <p>{instance.reply_message}</p>"""
                    recipient_list = [email_id]

                    form.instance.replied = True
                    form.instance.save()
                    
                    send_mail(
                    subject='Your Subject Here',
                    message='',  # Set an empty string for plain text content (not used in this case)
                    recipient_list=recipient_list,
                    html_message=html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL
                )

        super(ContactUsAdmin, self).save_related(request, form, formsets, change)

@admin.register(AdminReply)
class AdminReplyAdmin(admin.ModelAdmin):
    list_display = ('contact_us', 'admin_user', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('contact_us__email', 'admin_user__email')
    form = AdminReplyForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def save_model(self, request, obj, form, change):
        # Set admin_user to the current logged-in admin (if authenticated)
        if request.user and request.user.is_authenticated and not obj.admin_user:
            obj.admin_user = request.user
        else:
            # Handle the case where request.user is None or not authenticated
            # For example, you might want to raise an exception or log a warning
            raise ValueError("Cannot save AdminReply without a valid admin_user")

        obj.save()

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        # Ensure the contact_us instance is saved with replied set to True
        contact_us_instance = form.instance.contact_us
        if contact_us_instance:
            contact_us_instance.replied = True
            contact_us_instance.save()
    
    # def save_formset(self, request, form, formset, change):
    #     instances = formset.save(commit=False)

    #     for instance in instances:
    #         if not instance.admin_user:
    #             # Set admin_user to the current logged-in admin (if authenticated)
    #             if request.user and request.user.is_authenticated:
    #                 instance.admin_user = request.user
    #             else:
    #                 # Handle the case where request.user is None or not authenticated
    #                 # You can raise an exception or log a warning
    #                 instance.admin_user_id = None

    #         instance.save()

    #     formset.save_m2m()
 
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
