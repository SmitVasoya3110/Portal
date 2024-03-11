from django.urls import path, include
from .views import (loginAdmin, home, fetchStudents, 
            allStudents, fetchExams, examInfo, studentrecord,
            editQuestion, addQuestion, logoutAdmin, deleteQuestion
)
app_name="teacher"
urlpatterns = [
    path(r'portal/login/', loginAdmin, name='loginadmin'),
    path('portal/', home, name='adminhome'),
    path('all-students-data/', allStudents, name='all-students-data'),
    path('logoutadmin/', home, name='logoutadmin'),
    path('college-student/<id>', fetchStudents, name='college-student'),
    path('college-exam/', fetchExams, name="college_exam"),
    path('exam-info/<int:id>', examInfo, name="exam-info"),
    path('addquestion/<int:id>', addQuestion, name="addquestion"),
    path('edit-question/<int:exam_id>/<int:q_id>', editQuestion, name="edit-question"),
    path('delete-question/<int:exam_id>/<int:q_id>', deleteQuestion, name="delete-question"),
    path('studentrecords/<int:exam_id>/<int:college_id>', studentrecord, name="studentrecords"),
    path('logoutteacher/', logoutAdmin, name="logoutadmin")
]