from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course
from .serializers import CourseSerializer
import random
from rest_framework import status

from .service_externes import (
    get_place_details, get_distance_and_duration, get_weather,
    get_traffic_conditions, encoding_weather, encodage_traffic_conditions
)




@api_view(['POST'])
def estimation_demo(request):
    data = request.data
    departure_address = data.get('departure_address')
    arrival_address = data.get('arrival_address')
    distance_km = random.uniform(1,25)
    estimated_time = distance_km * 1.5
    estimated_price = round(distance_km * estimated_time * 0.40,1)
    if departure_address == arrival_address or departure_address is None or arrival_address is None:
        return f"Remplissez correctement les adresses"

    return Response({
        'departure_address':departure_address,
        'arrival_address':arrival_address,
        'distance_km':distance_km,
        'estimated_time':round(estimated_time,1),
        'estimated_price':estimated_price
    })


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def start_course(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        #serializer.save(user=request.user)
        serializer.save()
        return Response({"message":"Course Started Successfully",
                         "data":serializer.data})
    return Response(serializer.errors, status=400)



@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def course_history(request):
    course = Course.objects.all()
    # course = Course.objects.filter(user=request.user).order_by('-created_at')
    serializer = CourseSerializer(course, many=True)
    return Response(serializer.data)




class EstimationAPIView(APIView):
    def post(self, request):
        departure_place_id = request.data.get("departure_place_id")
        arrival_place_id = request.data.get("arrival_place_id")

        if not departure_place_id or not arrival_place_id:
            return Response({"error": "Les place_id de départ et d'arrivée sont requis."}, status=400)

        # Obtenir les coordonnées GPS
        lat1, lon1 = get_place_details(departure_place_id)
        lat2, lon2 = get_place_details(arrival_place_id)

        if not lat1 or not lat2:
            return Response({"error": "Impossible d'obtenir les coordonnées GPS."}, status=400)

        # Calculer la distance et le temps estimé
        distance_km, duration_min = get_distance_and_duration(lat1, lon1, lat2, lon2)
        if distance_km is None:
            return Response({"error": "Échec du calcul distance/durée."}, status=500)

        # Météo actuelle au point de départ
        temp, weather_desc = get_weather(lat1, lon1)
        weather_rain, weather_snow = encoding_weather(weather_desc)

        # Conditions de trafic
        traffic_level = get_traffic_conditions(lat1, lon1, lat2, lon2)
        traffic_low, traffic_medium = encodage_traffic_conditions(traffic_level)

        # Modèle ML
        features = [
            distance_km,
            duration_min,
            0.70,  # prix par km
            traffic_low,
            traffic_medium,
            weather_rain,
            weather_snow
        ]

        # chagement des modèles
        import joblib

        modele_rf = joblib.load("mon_modele_rf1.joblib")
        modele_linear = joblib.load("mon_modele_2.joblib")

        if distance_km > 50:
            price = modele_linear.predict([features])[0]
        else:
            price = modele_rf.predict([features])[0]

        return Response({
            "estimated_price": round(price, 2),
            "estimated_time": round(duration_min, 1),
            "distance_km": distance_km,
            "weather": weather_desc,
            "traffic": traffic_level
        }, status=status.HTTP_200_OK)
