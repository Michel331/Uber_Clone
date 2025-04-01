from django.urls import path
from .views import estimation,start_course,course_history

urlpatterns = [
	path('estimation/',estimation, name = 'estimation' ),
	path('start_course/',start_course, name = 'start_course'),
	path('course_history/',course_history, name = 'course_history')
]

