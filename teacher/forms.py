from student.models import Exam, Question, Choice
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import inlineformset_factory

from teacher.models import Teacher


ChoiceFormSet = inlineformset_factory(Question, Choice, fields=('text', 'is_correct'), extra=4, can_delete=False, max_num=4)



class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = "__all__"

class TeacherUpdateForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['branch']  # Add more fields as needed

class TeacherPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class TeacherAdminForm(ModelForm):
    class Meta:
        model = Teacher
        exclude = ('last_login',) 