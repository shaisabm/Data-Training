from django.db import models



# Create your models here.


class MasterDB(models.Model):
    topic = models.CharField(max_length=500, null=True, blank=True)
    zoom_id = models.CharField(max_length=100, null=True, blank=True)
    event_month = models.CharField(max_length=100, null=True, blank=True)
    event_date = models.CharField(max_length=100, null=True, blank=True)
    event_time = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    join_time = models.CharField(max_length=100, null=True, blank=True)
    leave_time = models.CharField(max_length=100, null=True, blank=True)
    duration = models.IntegerField(default=0, null=True, blank=True)
    attended = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ['first_name', 'last_name', 'zoom_id', 'email']

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
    json_validation_schema = models.JSONField(blank=True, null=True)


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
        return default_instance



    def __str__(self):
        return str(self.ai_model)





