from django.db import models

# Create your models here.

class Event(models.Model):
    event_name = models.CharField(max_length=100, null=True, blank=True)
    zoom_id = models.CharField(max_length=100, unique=True)


class Registration(models.Model):
    event_name = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_registrations')
    zoom_id = models.ForeignKey(Event, on_delete=models.CASCADE ,related_name='zoom_registrations')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    registration_time = models.DateTimeField()
    approved = models.BooleanField(default=False)
    status = models.CharField(max_length=100)
    participated = models.BooleanField(default=False, null=True, blank=True)



class Participant(models.Model):
    zoom_id = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='zoom_participants')
    event_name = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_participants')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    joined_time = models.DateTimeField()
    leave_time = models.DateTimeField()
    duration = models.DurationField()
    guest = models.BooleanField(default=False)
    in_waiting_room = models.BooleanField(default=False)







