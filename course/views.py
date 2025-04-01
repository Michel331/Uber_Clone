from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer
import random

@api_view(['POST'])
def estimation(request):
	data = request.data
	departure_address = data.get('departure_address','Adresse de depart introuvable')
	arrival_address = data.get('arrival_address','Adresse finale introuvable')
	distance_km = random.uniform(1,25)
	estimated_time = distance_km * 1.5
	estimated_price = round(distance_km * estimated_time * 0.40,1)

	return Response({
		'departure_address':departure_address,
		'arrival_address':arrival_address,
		'distance_km':distance_km,
		'estimated_time':round(estimated_time,1),
	 	'estimated_price':estimated_price
	})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_course(request):
	serializer = CourseSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save(user=request.user)
		return Response({"message":"Course Started Successfully", "data":serializer.data})
	return Response(serializer.errors, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_history(request):
	course = Course.objects.filter(user=request.user).order_by('-created_at')
	serializer = CourseSerializer(course, many=True)
	return Response(serializer.data)
