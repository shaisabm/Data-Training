from django.db import models
import json
import os


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



class DefaultAiConfig(models.Model):
    api_key = models.CharField(max_length=200, blank=True, null=True)
    base_url = models.CharField(max_length=100, blank=True, null=True)
    system_instructions = models.TextField(blank=True, null=True)


    def save(self, *args, **kwargs):
        if type(self).objects.exists() and not self.pk:
            raise ValueError("Only one AI configuration instance is allowed")
        super().save(*args, **kwargs)




class AiModel(models.Model):
    ai_model = models.CharField(null=True, max_length=50)

    @classmethod
    def get_defaults(cls):
        if not DefaultAiConfig.objects.exists():
            raise ValueError("No default configurations found. Please create a default config instance.")
        default_instance = DefaultAiConfig.objects.filter().first()
        return {'api_key': default_instance.api_key,
                'base_url': default_instance.base_url,
                'system_instructions': default_instance.system_instructions}



    def __str__(self):
        return str(self.ai_model)





