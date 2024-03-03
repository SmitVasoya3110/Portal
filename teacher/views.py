from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from student.models import Student, College, Exam, Question, Choice, ExamResult

# Create your views here.
def loginAdmin(request):
    auth_form = AuthenticationForm()
    if request.method == "POST":
        print(request.POST)
        user = authenticate(request, email = request.POST['username'], password=request.POST['password'])
        print(user)
        if user:
            login(request, user)
            return redirect(reverse('teacher:home'))

    context= {'auth_form':auth_form}
    return render(request, 'teacher/teacher_login.html', context)

def home(request):
    college = College.objects.get(teacher_id=request.user.teacher.teacher_id)
    # college_count = college_list.count()
    total_students = Student.objects.filter(college=college).count()
    total_exams = Exam.objects.filter(college=college).count()
    context = {
        'college' : college,
        'students' : total_students,
        'exam_count' : total_exams
    }
    return render(request, 'teacher/dashboard.html', context)