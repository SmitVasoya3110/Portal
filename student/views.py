
import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from contact.models import Feedback
from student.models import CustomUser,Exam, Choice, ExamResult, Question, Record, Student
from .forms import UserCreationForm, StudentCreationForm, StudentLoginForm

global question_list
global answer_list

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        student_form = StudentCreationForm(request.POST)

        if user_form.is_valid() and student_form.is_valid():
            # Save the user
            user = user_form.save()
            # Save the student with the user reference
            student = student_form.save(user=user,commit=False)
            student.user = user
            student.save()

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect(reverse('student:student_login'))  # Adjust the 'login' to the actual URL name for your login view
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')

    else:
        user_form = UserCreationForm()
        student_form = StudentCreationForm()

    return render(request, 'student/student_registration.html', {'user_form': user_form, 'student_form': student_form})

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('student:student_dashboard')  # Adjust this to the actual URL name for the student dashboard
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = StudentLoginForm()

    return render(request, 'student/student_login.html', {'form': form})

@login_required(login_url='/student/login')
def student_dashboard(request):
    print(request.user)
    try:
        student = request.user.student
        college = student.college

        # Get upcoming exams in the next 30 minutes
        upcoming_exams = Exam.objects.filter(
            college=college,
            # start_time__gte=timezone.now(),
            # start_time__lte=timezone.now() + timezone.timedelta(minutes=30)
        ).order_by('start_time')

        context = {
            'student': student,
            'college': college,
            'upcoming_exams': upcoming_exams,
        } 
        if request.method == "POST":
            print(request.POST) 
            print(end="================================================" )
            form_exam = request.POST['exam']
            exam = Exam.objects.get(id=form_exam)
            context = {
            'student': student,
            'college': college,
            'exam': exam,
            }
            return render(request, 'student/instruction.html', context)
        return render(request, 'student/student_dashboard.html', context)
    except CustomUser.DoesNotExist:
        messages.error(request, "Student does not exists!")
        logout(request)
        return redirect("student:student_login")
    except Student.DoesNotExist:
        messages.error(request, "Student does not exists!")
        logout(request)
        return redirect("student:student_login")

@login_required(login_url='/student/login')
def exam(request, id):
    try:
        questions = Question.objects.filter(exam__id=id)
        global answer_list
        answer_list = []
        option_list = []
        global question_list
        question_list = list(questions)
        check = Record.objects.filter(student_id=request.user.id, exam_id=id)
        if check.count() > 0:
            return messages(request, "You have already given the exam")
        for question in question_list:
            Record.objects.create(student_id=request.user.id, exam_id=id, question_id=question.id)
            option = Choice.objects.filter(question=question.id)
            option_list.extend(list(option))
        exam_question = question_list[:]
        print(option_list)
        random.shuffle(question_list)
        context = {'questions': exam_question, 'questions_page': exam_question, 'option_list': option_list, 'exam_id':id}
        return render(request, 'student/exam.html', context)
    except IntegrityError as e:
        print(e)
        return redirect('home')
    except TypeError as e:
        print(e)
        return redirect('home')

@login_required(login_url='/student/login')    
def saveans(request):
    print("Save Ans is Called")
    print(request.GET)
    question_id = request.GET['qid']
    answer = request.GET['ans']
    exam_id = request.GET['eid']
    Record.objects.filter(question_id=question_id, exam_id=exam_id, student_id=request.user.id).update(answer=answer)
    return JsonResponse({"message":"Record added"})

@login_required(login_url='/student/login')
def result(request,id):
    score = 0
    global question_list
    compare_list = question_list[:]
    for question in compare_list:
        record = Record.objects.filter(question_id=question.id).order_by('-created_at').first()
        true_answer = Choice.objects.get(question=question, is_correct=True)
        print(true_answer)
        print(true_answer.id)
        print(record)
        print(record.answer)
        print(int(record.answer) == int(true_answer.id))
        if int(record.answer) == int(true_answer.id):

            score += 5
    exam = Exam.objects.get(pk=id)
    student = Student.objects.get(user=request.user)
    exam_result = ExamResult.objects.create(user=request.user, student=student, exam=exam, score=score, marks=len(compare_list)*5)
    return render(request, 'student/result.html', {'score':score, "total_score":5*len(question_list)})
    
@login_required(login_url='/student/login')
def signout(request):
    logout(request)
    return redirect('student:login')

def enrollment_form(request):
    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')
        return redirect('student:view_student_details', enrollment_id=enrollment_id)
    return render(request, 'student/student_score.html')

def view_student_details(request, enrollment_id):
    try:
        student = Student.objects.get(user__email=enrollment_id)
        exam_results = ExamResult.objects.filter(student=student)
        
        return render(request, 'student/student_exam_result.html', {'student': student, 'exam_results': exam_results})
    except Student.DoesNotExist:
        messages.error(request,"student with the given email not found!")
        return redirect('student:results')


def landing_page(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')[:5]  # Change 5 to the desired number of feedbacks
    return render(request, 'home.html',{'feedbacks': feedbacks})