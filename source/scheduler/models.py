from django.db import models

# Create your models here.

class Name(models.Model):
    name_first = models.CharField(max_length=50)
    name_last = models.CharField(max_length=50)