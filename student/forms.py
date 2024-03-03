from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Student
from django.contrib.auth.forms import AuthenticationForm


CustomUser = get_user_model()
print(CustomUser)
class UserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name','password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class StudentCreationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('college', 'enrollment_id', 'branch')
        
    
    def clean_enrollment_id(self):
        enrollment_id = self.cleaned_data.get('enrollment_id')
        if not enrollment_id.isdigit():
            raise ValidationError("Student ID must be a number.")
        return enrollment_id
    
    def save(self, user, commit=True):
        print(type(user))
        # Check if the user already has an associated student
        user.is_student = True

        if commit:
            user.save()

        student = Student.objects.create(
            user=user,
            college=self.cleaned_data['college'],
            enrollment_id=self.cleaned_data['enrollment_id'],
            branch=self.cleaned_data['branch'],
        )

        return student
    
class StudentLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
