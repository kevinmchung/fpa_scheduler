from django.db import models

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

class Provider(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	abbrev = models.CharField(max_length=3)

	num_work_days = models.TextField()
	vacation_days = models.TextField()
	office_ranges = models.TextField()

	def __str__(self):
		return "{}, {} ({})".format(self.last_name, self.first_name, self.abbrev)

class Office(models.Model):
	name = models.CharField(max_length=50)
	abbrev = models.CharField(max_length=10)

	provider_range = models.TextField()
	weekend = models.BooleanField()

	def __str__(self):
		return "{} ({})".format(self.name, self.abbrev)