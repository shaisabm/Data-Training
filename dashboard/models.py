from django.db import models
import json

# Create your models here.


class MasterDB(models.Model):
    topic = models.CharField(max_length=500, null=True, blank=True)
    zoom_id = models.CharField(max_length=100)
    event_month = models.CharField(max_length=100)
    event_date = models.CharField(max_length=100)
    event_time = models.CharField(max_length=100)
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


class AiModel(models.Model):
    ai_model = models.CharField(null=True , max_length=50)
    api_key = models.CharField(max_length=200)
    base_url = models.CharField(max_length=100)
    system_instructions = models.TextField()

    def __str__(self):
        return str(self.ai_model)


