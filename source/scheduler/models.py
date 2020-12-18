from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Make your models here

class Provider(models.Model):
	name_first = models.CharField(max_length=50)
	name_last = models.CharField(max_length=50)
	#abbrev = models.CharField(max_length=3)
	abbrev = models.CharField(max_length=3, unique=True,)
	days_per_week = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return "{}, {}".format(self.name_last, self.name_first)


class Location(models.Model):
	name = models.CharField(max_length=50)
	abbrev = models.CharField(max_length=5, unique=True,)
	provider_min = models.PositiveSmallIntegerField(default=0)
	provider_max = models.PositiveSmallIntegerField(default=0)
	weekend = models.BooleanField()
	num_providers_weekend = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return "{}".format(self.name)


class ProviderVacation(models.Model):
	provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
	start_date = models.DateField()
	end_date = models.DateField()

	def __str__(self):
		return "{} | {} - {}".format(self.provider, self.start_date, self.end_date)


class ProviderLocationMax(models.Model):
	provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)
	provider_at_location_max_days = models.PositiveSmallIntegerField(default=5, validators=[MaxValueValidator(5), MinValueValidator(0)])

	def __str__(self):
		return "{} @ {} | {}".format(self.provider,self.location,self.provider_at_location_max_days)

