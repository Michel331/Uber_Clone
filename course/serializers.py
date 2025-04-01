from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = '__all__'


"""
curl -X POST http://localhost:8000/api/start_course/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQzMzAyMzMyLCJpYXQiOjE3NDMzMDIwMzIsImp0aSI6IjNhZTlhOWQ2ODFkYzRiYjZhZDAxMzlkMmZkMjMwMzJmIiwidXNlcl9pZCI6MX0._7L-GhSP6edhwwCZJ4UXQcwfOXXzJkOenhLVl2BWC20" \
  -d '{
    "departure_address": "Matoto",
    "arrival_address": "Kaloum",
    "distance_km": 7.2,
    "estimated_time": 21.5,
    "estimated_price": 1520
  }'
"""