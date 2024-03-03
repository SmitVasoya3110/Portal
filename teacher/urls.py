from django.urls import path, include
from .views import loginAdmin, home

app_name="teacher"
urlpatterns = [
    path(r'portal/login/', loginAdmin, name='loginadmin'),
    path('portal/', loginAdmin, name='adminhome'),

]