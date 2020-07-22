from django.db import models
#from names import models

# Make your models here
'''
class Name(models.Model):

    # *** Name model has been recreated in Names app
    # Not needed here anymore (but need to figure out how to remove from database)

    name_first = models.CharField(max_length=50)
    name_last = models.CharField(max_length=50)

    def __str__(self):
        return "{} {}".format(self.name_first, self.name_last)

'''

'''class Preference(models.Model):

	provider = models.ForeignKey('names.Name', on_delete=models.CASCADE)
'''


class Provider(models.Model):
	name_first = models.CharField(max_length=50)
	name_last = models.CharField(max_length=50)
	abbrev = models.CharField(max_length=3)
	#abbrev = models.CharField(max_length=3, unique=True, error_messages={'unique':"This abbreviation is already registered."})
	days_per_week = models.PositiveSmallIntegerField(default=0)

	def __str__(self):
		return "{}, {}".format(self.name_last, self.name_first)


class Location(models.Model):
	name = models.CharField(max_length=50)
	abbrev = models.CharField(max_length=5)
	provider_min = models.PositiveSmallIntegerField(default=0)
	provider_max = models.PositiveSmallIntegerField(default=0)
	weekend = models.BooleanField()

	def __str__(self):
		return "{}".format(self.name)


class ProviderVacation(models.Model):
	provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
	vacation_date = models.DateField()


class ProviderLocationMax(models.Model):
	provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)
	provider_location_max = models.PositiveSmallIntegerField(default=0)



