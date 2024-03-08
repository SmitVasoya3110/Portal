from django.urls import path
from .views import contact_us, feedback

app_name = "contact"
urlpatterns = [
    path('contact_us/', contact_us, name='contact_us'),
     path('feedback/', feedback, name='feedback')
    # Add other URL patterns as needed
]