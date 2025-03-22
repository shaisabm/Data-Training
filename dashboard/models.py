from django.db import models


class MasterDB(models.Model):
    """
    Main database model for storing participant attendance information.

    This model stores information about participants who attended events,
    including their personal details and attendance metrics.
    """
    topic = models.CharField(max_length=500, null=True, blank=True)  # Event topic/title
    zoom_id = models.CharField(max_length=100, null=True, blank=True)  # Unique identifier for the Zoom meeting
    event_month = models.CharField(max_length=100, null=True, blank=True)  # Month when event occurred
    event_date = models.CharField(max_length=100, null=True, blank=True)  # Date of the event
    event_time = models.CharField(max_length=100, null=True, blank=True)  # Time of the event
    first_name = models.CharField(max_length=100, null=True, blank=True)  # Participant's first name
    last_name = models.CharField(max_length=100, null=True, blank=True)  # Participant's last name
    email = models.EmailField(null=True, blank=True)  # Participant's email address
    join_time = models.CharField(max_length=100, null=True, blank=True)  # When participant joined the event
    leave_time = models.CharField(max_length=100, null=True, blank=True)  # When participant left the event
    duration = models.IntegerField(default=0, null=True, blank=True)  # Duration of attendance in minutes
    attended = models.CharField(max_length=100, null=True, blank=True)  # Attendance status (e.g., "Yes", "No")

    class Meta:
        # Ensure no duplicate entries for the same person at the same event
        unique_together = ['first_name', 'last_name', 'zoom_id', 'email']


class ExcludedIndividual(models.Model):
    """
    Model to track emails that should be excluded from processing.

    These individuals will be filtered out when processing attendance data.
    """
    email = models.EmailField()  # Email address to exclude

    @classmethod
    def get_all_emails(cls):
        """
        Retrieve all excluded email addresses as a flat list.

        Returns:
            QuerySet: List of all excluded email addresses
        """
        return cls.objects.values_list('email', flat=True)

    def __str__(self):
        """String representation of the model instance."""
        return self.email


class DefaultAiConfig(models.Model):
    """
    Singleton model to store default configuration for AI models.

    This model is designed to have only one instance that stores
    the configuration parameters used by all AI models.
    """
    api_key = models.CharField(max_length=200, blank=True, null=True)  # API key for AI service
    base_url = models.CharField(max_length=100, blank=True, null=True)  # Base URL for API requests
    system_instructions = models.TextField(blank=True, null=True)  # Instructions for the AI model
    json_validation_schema = models.JSONField(blank=True, null=True)  # Schema to validate AI responses

    def save(self, *args, **kwargs):
        """
        Override save method to ensure only one instance exists.

        Raises:
            ValueError: If attempting to create a second instance
        """
        if type(self).objects.exists() and not self.pk:
            raise ValueError("Only one AI configuration instance is allowed")
        super().save(*args, **kwargs)


class AiModel(models.Model):
    """
    Model to represent different AI models available for processing data.

    Each instance represents a specific AI model that can be used
    to process registration and participant data.
    """
    ai_model = models.CharField(null=True, max_length=50)  # Name or identifier of the AI model

    @classmethod
    def get_defaults(cls):
        """
        Get the default AI configuration.

        Returns:
            DefaultAiConfig: The default configuration instance

        Raises:
            ValueError: If no default configuration exists
        """
        if not DefaultAiConfig.objects.exists():
            raise ValueError("No default configurations found. Please create a default config instance.")
        default_instance = DefaultAiConfig.objects.filter().first()
        return default_instance

    def __str__(self):
        """String representation of the model instance."""
        return str(self.ai_model)