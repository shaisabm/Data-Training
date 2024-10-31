from modulefinder import Module

from django.db import models

# Create your models here.


#
# class Registration(models.Model):
#     event_name = models.CharField(max_length=500, null=True, blank=True)
#     zoom_id = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField()
#     registration_time = models.CharField(max_length=100)
#     approval_status = models.CharField(max_length=100)
#     participated = models.BooleanField(default=False, null=True, blank=True)
#
#
#
# class Participant(models.Model):
#     event_name = models.CharField(max_length=500, null=True, blank=True)
#     zoom_id = models.CharField(max_length=100)
#     full_name = models.CharField(max_length=100)
#     email = models.EmailField()
#     joined_time = models.DateTimeField()
#     leave_time = models.DateTimeField()
#     duration = models.IntegerField(default=0)
#     guest = models.BooleanField(default=False)
#     in_waiting_room = models.BooleanField(default=False)

class MasterDB(models.Model):
    topic = models.CharField(max_length=500, null=True, blank=True)
    zoom_id = models.CharField(max_length=100)
    event_date = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    registration_time = models.CharField(max_length=100)
    join_time = models.CharField(max_length=100)
    leave_time = models.CharField(max_length=100)
    duration = models.IntegerField(default=0, null=True, blank=True)
    attended = models.CharField(max_length=100)



class ExcludedIndividual(models.Model):
    email = models.EmailField()

    @classmethod
    def get_all_emails(cls):
        return cls.objects.values_list('email', flat=True)

    def __str__(self):
        return self.email








