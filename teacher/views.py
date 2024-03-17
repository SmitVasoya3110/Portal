from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from student.models import Record, Student, College, Exam, Question, Choice, ExamResult
from teacher.forms import ChoiceForm, ChoiceFormSet, QuestionForm, TeacherPasswordChangeForm, TeacherUpdateForm
from teacher.models import Teacher
from django.utils import timezone
from django.contrib import messages

# Create your views here.
def loginAdmin(request):
    auth_form = AuthenticationForm()
    context= {'auth_form':auth_form}
    try:
        if request.method == "POST":
            print(request.POST)
            user = authenticate(request, email = request.POST['username'], password=request.POST['password'])
            print(user)
            if user:
                login(request, user)
                user.last_login = timezone.now()
                teacher = Teacher.objects.get(user=user)
                teacher.last_login = user.last_login
                teacher.save()
                return redirect(reverse('teacher:adminhome'))
            else:
                messages.error(request, "Teacher is not registered with us!")
        return render(request, 'teacher/teacher_login.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher is not registered with us!")
        return render(request, 'teacher/teacher_login.html', context)
    
def home(request):
    print(request.user)
    try:
        teacher = Teacher.objects.get(user=request.user)
    
        college = teacher.college
        # college_count = college_list.count()
        total_students = Student.objects.filter(college=college).count()
        total_exams = Exam.objects.filter(college=college).count()
        print(total_exams, total_students, college)
        context = {
            'college' : college,
            'student_count' : total_students,
            'exam_count' : total_exams,
            'college_list': [college]
        }
        return render(request, 'teacher/dashboard.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, "Please Login again to proceed")
        return redirect('teacher:loginadmin')
    
def fetchStudents(request, id):
    students = Student.objects.filter(college=id)
    context = {'students':students}
    return render(request, 'teacher/studentlist.html', context)

def allStudents(request):
    try:

        teacher = Teacher.objects.get(user=request.user)
        all_students = Student.objects.filter(college=teacher.college)

        context = {'students':all_students}
        return render(request, 'teacher/studentlist.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, "Please Login again to proceed")
        return redirect('teacher:loginadmin')
    
def fetchExams(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        exam_list = Exam.objects.filter(college=teacher.college)
        context = {'exam_list':exam_list}
        print(context)
        return render(request, 'teacher/college_exam.html', context)
    except Teacher.DoesNotExist:
        messages.error(request, "Please Login again to proceed")
        return redirect('teacher:loginadmin')
    
def examInfo(request, id):
    question_list = Question.objects.filter(exam=id)
    option_list = []
    for ques in question_list:
        try:
            option = Choice.objects.filter(question = ques)


            # print(type(options))
            # if len(options) > 1:    
            #     for option in options:
            #         if option.question.id == ques.id:
            #             option_list.append(option)
            # else:
            # option = options
            option_list.append({ques.id:{'options':option, 'correct_ans':option.get(is_correct=True), 'counter':range(4-option.count())}})
        except:
            pass
        
    context = {'question_list':question_list, 'option_list':option_list, 'exam_id':id}
    return render(request, 'teacher/exam_info.html', context)

def studentrecord(request,exam_id, college_id):
    students = Student.objects.filter(college=college_id)
    exam = Exam.objects.get(id=exam_id)
    score_list = []
    for student in students:
        score = 0
        # print(student, student.pk)
        records = Record.objects.filter(exam_id=exam_id,student_id=student.pk).exclude(answer='N').distinct()
        for record in records:
            question = Question.objects.get(id=record.question_id)
            correct_choice = Choice.objects.get(question=question, is_correct=True)
            # print(correct_choice, correct_choice.id, record.answer)
            if int(correct_choice.id) == int(record.answer):
                score += 2
        score_list.append(score)
    context={'students':students, 'score_list':score_list, 'exam':exam}
    return render(request, 'teacher/studentrecord.html', context)

def editQuestion(request, exam_id, q_id):
     # Get the exam instance
    try:
        exam = get_object_or_404(Exam, pk=exam_id)

        # Get the question instance
        question = get_object_or_404(Question, pk=q_id, exam=exam)

        if request.method == 'POST':
            question_form = QuestionForm(request.POST, instance=question)
            choice_formset = ChoiceFormSet(request.POST, instance=question)

            if question_form.is_valid() and choice_formset.is_valid():
                question = question_form.save()
                choices = choice_formset.save(commit=False)
                
                for choice in choices:
                    choice.question = question
                    choice.save()

                return redirect('teacher:exam-info',id=exam_id)  # Redirect to a success page

        else:
            question_form = QuestionForm(instance=question)
            choice_formset = ChoiceFormSet(instance=question)
        context = {
            'question_form': question_form,
            'choice_form': choice_formset,
            'exam': exam,
            'question': question
        }   
        return render(request, 'teacher/update_question.html', context)
    except Exam.DoesNotExist:
        messages.error("The Exam is not found!")
        return redirect('teacher:"college_exam')
    except Question.DoesNotExist:
        messages.error("The Question does not exists")
        return redirect('teacher:exam-info',id=exam_id)
    except Exception as e:
        messages.error("Internal Server Error")
        return redirect('teacher:"college_exam')
    
def deleteQuestion(request, exam_id, q_id):
     # Get the exam instance
    try:
        exam = get_object_or_404(Exam, pk=exam_id)

        # Get the question instance
        question = get_object_or_404(Question, pk=q_id, exam=exam)

        question.delete()

        return  redirect(reverse('teacher:exam-info',kwargs={'id' : exam_id}))
    except Question.DoesNotExist:
        messages.error(request, "Question Not Found")
        return redirect(reverse('teacher:exam-info',kwargs={'id' : exam_id}))
    except Exception as e:
        print(e)
        return  redirect(reverse('teacher:exam-info',kwargs={'id' : exam_id}))

    # if request.method == 'POST':
    #     question_form = QuestionForm(request.POST, instance=question)
    #     choice_formset = ChoiceFormSet(request.POST, instance=question)

    #     if question_form.is_valid() and choice_formset.is_valid():
    #         question = question_form.save()
    #         choices = choice_formset.save(commit=False)
            
    #         for choice in choices:
    #             choice.question = question
    #             choice.save()

    #         return redirect('teacher:exam-info',id=exam_id)  # Redirect to a success page

    # else:
    #     question_form = QuestionForm(instance=question)
    #     choice_formset = ChoiceFormSet(instance=question)
    # context = {
    #     'question_form': question_form,
    #     'choice_form': choice_formset,
    #     'exam': exam,
    #     'question': question
    # }
    # return render(request, 'teacher/update_question.html', context)

# def editQuestion(request, exam_id, q_id):
#     question = Question.objects.get(id=q_id)
#     option = Choice.objects.get(question=q_id)
    
#     question_form = QuestionForm(instance=question)
#     option_form = ChoiceForm(instance=option)

#     if request.method == "POST":
#         question_form = QuestionForm(request.POST, instance=question) 
#         option_form = ChoiceForm(request.POST, instance=option)
#         if question_form.is_valid() and option_form.is_valid():
#             question_form.save()
#             option_form.save()
#         return redirect('adminapp:exam-info', id=exam_id)
#     context = {'question_form':question_form, 'option_form':option_form}
#     return render(request, 'adminapp/update_question.html', context)


def addQuestion(request, id):
    try:
        exam = Exam.objects.get(id=id)
        if request.method == 'POST':
            question_form = QuestionForm(request.POST)
            choice_formset = ChoiceFormSet(request.POST, instance=Question())

            if question_form.is_valid() and choice_formset.is_valid():
                # Save the question form
                question = question_form.save()

                # Save the choice formset with the question instance
                choices = choice_formset.save(commit=False)
                for choice in choices:
                    choice.question = question
                    choice.save()

                return redirect('teacher:exam-info',id=id)  # Redirect to a success page

        else:
            question_form = QuestionForm(initial={'exam':exam})
            choice_formset = ChoiceFormSet(instance=Question())

        return render(request, 'teacher/add_question.html', {'question_form': question_form, 'choice_formset': choice_formset})
    except Exam.DoesNotExist:
        messages.error("The Exam is not found!")
        return redirect('teacher:"college_exam')
    except Exception as e:
        print(e)
        messages.error("Internal Server Error!")
        return  redirect('teacher:"college_exam')
# def addQuestion(request, id):
#     exam = Exam.objects.get(id=id)
#     question_form = QuestionForm(initial={'exam':exam})
    
#     if request.method == 'POST':
#         question_form = QuestionForm(request.POST)
#         if question_form.is_valid():
#             # question = question_form.cleaned_data['question_text']
#             question = question_form.save()
#             option_form = ChoiceFormSet(instance=question)
#             context = {'option_form':option_form, 'exam_id':id}
#             return render(request, 'teacher/add_option.html', context)

#     question_form = QuestionForm(initial={'exam':exam})
#     choice_formset = ChoiceFormSet(instance=Question())
#     context = {'question_form':question_form}
#     return render(request, 'teacher/add_question.html', context)

def addOption(request, id):
    if request.method == 'POST':
        choices = ChoiceFormSet(request.POST)
        if ChoiceFormSet.is_valid():
            ChoiceFormSet.save()
        return redirect('adminapp:exam-info',id=id)
    else:
        return HttpResponse("It only can be seen after adding new questions")

def update_teacher_details(request):
    try:
        
        teacher = Teacher.objects.get(user=request.user)  # Assuming the user is logged in and associated with a teacher profile
        if request.method == 'POST':
            if 'update_details' in request.POST:
                details_form = TeacherUpdateForm(request.POST, instance=teacher)
                if details_form.is_valid():
                    details_form.save()
                    return redirect('teacher:adminhome')  # Redirect to teacher panel after successful update
            elif 'change_password' in request.POST:
                password_form = TeacherPasswordChangeForm(request.user, request.POST)
                if password_form.is_valid():
                    password_form.save()
                    update_session_auth_hash(request, password_form.user)
                    return redirect('teacher:adminhome')  # Redirect to teacher panel after successful password change
        else:
            details_form = TeacherUpdateForm(instance=teacher)
            password_form = TeacherPasswordChangeForm(request.user)
        return render(request, 'teacher/update_teacher.html', {'details_form': details_form, 'password_form': password_form, 'teacher': teacher})
    except Teacher.DoesNotExist:
        messages.error(request, "Please Login again to proceed")
        return redirect('teacher:loginadmin')
    
def logoutAdmin(request):
    logout(request)
    return redirect('/')
