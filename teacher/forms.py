from student.models import Exam, Question, Choice
from django.forms import ModelForm
from django.forms import inlineformset_factory


ChoiceFormSet = inlineformset_factory(Question, Choice, fields=('text', 'is_correct'), extra=4)


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = "__all__"

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = "__all__"
