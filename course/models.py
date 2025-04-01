from django.db import models
from account.models import User

# Creation of ours differents models

class Course(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	departure_address = models.CharField(max_length=250)
	arrival_address = models.CharField(max_length=250)
	distance_km = models.FloatField()
	estimated_time = models.FloatField()
	estimated_price = models.FloatField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return (f"Depart : {self.departure_address}  ➡️ "
				f"- Arrivee : {self.arrival_address} "
				f"- Distance : {round(self.distance_km,2)} km")




