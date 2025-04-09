from django.urls import path
from .views import estimation_demo,start_course,course_history, EstimationAPIView

urlpatterns = [
	path('estimation/',EstimationAPIView.as_view() , name = 'estimation_api' ),
	path('start_course/',start_course, name = 'start_course'),
	path('course_history/',course_history, name = 'course_history')
]

