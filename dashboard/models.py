from django.db import models

# Create your models here.



class Registration(models.Model):
    event_name = models.CharField(max_length=500, null=True, blank=True)
    zoom_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    registration_time = models.CharField()
    approval_status = models.CharField(max_length=100)
    participated = models.BooleanField(default=False, null=True, blank=True)



class Participant(models.Model):
    event_name = models.CharField(max_length=500, null=True, blank=True)
    zoom_id = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    joined_time = models.DateTimeField()
    leave_time = models.DateTimeField()
    duration = models.IntegerField(default=0)
    guest = models.BooleanField(default=False)
    in_waiting_room = models.BooleanField(default=False)







