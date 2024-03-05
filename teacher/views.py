from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from student.models import Record, Student, College, Exam, Question, Choice, ExamResult
from teacher.forms import ChoiceForm, ChoiceFormSet, QuestionForm
from teacher.models import Teacher

# Create your views here.
def loginAdmin(request):
    auth_form = AuthenticationForm()
    if request.method == "POST":
        print(request.POST)
        user = authenticate(request, email = request.POST['username'], password=request.POST['password'])
        print(user)
        if user:
            login(request, user)
            return redirect(reverse('teacher:adminhome'))

    context= {'auth_form':auth_form}
    return render(request, 'teacher/teacher_login.html', context)

def home(request):
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

def fetchStudents(request, id):
    students = Student.objects.filter(college=id)
    context = {'students':students}
    return render(request, 'teacher/studentlist.html', context)

def allStudents(request):
    teacher = Teacher.objects.get(user=request.user)
    all_students = Student.objects.filter(college=teacher.college)

    context = {'all_students':all_students}
    return render(request, 'teacher/studentlist.html', context)

def fetchExams(request):
    teacher = Teacher.objects.get(user=request.user)
    exam_list = Exam.objects.filter(college=teacher.college)
    context = {'exam_list':exam_list}
    print(context)
    return render(request, 'teacher/college_exam.html', context)

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

def logoutAdmin(request):
    logout(request)
    return redirect('/')
