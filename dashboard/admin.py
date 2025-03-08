from django.contrib import admin
from .models import AiModel, DefaultAiConfig, MasterDB
# Register your models here.

admin.site.register(AiModel)
admin.site.register(DefaultAiConfig)
admin.site.register(MasterDB)

