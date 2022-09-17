from django.db import models


# Create your models here.
class Face(models.Model):
    face_id = models.CharField(max_length=255)
    no_of_faces = models.CharField(max_length=255)
    emotions = models.CharField(max_length=500)
class Face_static(models.Model):
    no_of_faces = models.CharField(max_length=255)
class ReportData(models.Model):
    emotion = models.CharField(max_length=500)
    date = models.DateField()


