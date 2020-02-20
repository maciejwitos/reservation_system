from django.db import models
import datetime


class Room(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    projector = models.BooleanField(null=True)


class Reservation(models.Model):
    date = models.DateTimeField()
    comment = models.TextField(null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

