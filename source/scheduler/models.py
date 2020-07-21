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

	num_work_days = models.IntegerField(default=0)
	#vacation_days = models.TextField()
	#office_ranges = models.TextField()

	def __str__(self):
		return "{}, {}".format(self.name_last, self.name_first)
		#return "{}, {} ({})".format(self.name_last, self.name_first, self.abbrev)


class Location(models.Model):
	name = models.CharField(max_length=50)
	abbrev = models.CharField(max_length=10)

	provider_range = models.TextField()
	weekend = models.BooleanField()

	def __str__(self):
		return "{}".format(self.name)