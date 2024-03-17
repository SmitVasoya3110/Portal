from django.urls import path, include
from .views import register, student_login, student_dashboard, exam, saveans, result, signout, enrollment_form, view_student_details

app_name="student"
urlpatterns = [
    path('register/', register, name="student_registration"),
    path('login/', student_login, name='student_login'),
    path('dashboard/', student_dashboard, name='student_dashboard'),
    path('exam/<id>', exam, name='start_exam'),
    path('saveans/', saveans, name='start_exam'),
    path('result/<id>', result, name='result'),
    path('results/', enrollment_form, name='results'),
    path('student-details/<str:enrollment_id>/', view_student_details, name='view_student_details'),
    path('logout/', signout, name='logout'),
]