
from django.shortcuts import render
import pandas as pd
from dashboard.models import Registration
from django.utils import timezone
from .handle_uploads import registration_upload, participant_upload


def home(request):
    if request.method == "POST":
        participant_files = request.FILES.getlist('participant_files')
        registration_files = request.FILES.getlist('registration_files')
        registration_upload.registration_upload(registration_files)
        participant_upload.participant_upload(participant_files)





    return render(request, 'dashboard/home.html', {})
