from django import forms

from contact.models import AdminReply
from student.forms import CustomUser

class AdminReplyForm(forms.ModelForm):
    class Meta:
        model = AdminReply
        fields = ['reply_message']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     # Set the admin_user field to the current logged-in admin (if authenticated)
    #     if self.instance and not self.instance.admin_user_id:
    #         user = getattr(self, 'current_user', None)
    #         if user and user.is_authenticated:
    #             self.instance.admin_user = user
    #             self.fields['admin_user'].widget.attrs['readonly'] = True
    #     admin_user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), widget=forms.HiddenInput())