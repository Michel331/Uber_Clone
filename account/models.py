from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import BaseUserManager


# Create your models here.
class CustomUserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError("The Email field must be set")
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('user_type', 'CUSTOMER')  # ou DRIVER si tu préfères

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
	username = None

	email = models.EmailField(unique=True)

	USER_TYPE_CHOICES = (
		("DRIVER", "Driver"),
		("CUSTOMER", "Customer"),
	)

	user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default="CUSTOMER")
	phone = models.CharField(max_length=15, unique=True)
	profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

	USERNAME_FIELD = 'email'

	REQUIRED_FIELDS = ['user_type', 'phone']

	objects = CustomUserManager()

	def get_full_name(self):
		super().get_full_name()

	def __str__(self):
		return f"{self.email} - Nom Complet : {self.get_full_name()}"
