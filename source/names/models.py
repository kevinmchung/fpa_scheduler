from django.db import models
from django.urls import reverse

# Make your models here

class Name(models.Model):

    name_first = models.CharField(max_length=50)
    name_last = models.CharField(max_length=50)

    def __str__(self):
        return "{} {}".format(self.name_first, self.name_last)

    def get_absolute_url(self):
        return reverse('names:detail', kwargs={'pk': self.pk})
