from django.db import models


# Create your models here.
class Face(models.Model):
    no_of_faces = models.CharField(max_length=255)
    emotions = models.CharField(max_length=500)
