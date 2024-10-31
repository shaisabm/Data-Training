import json
from django.shortcuts import render, redirect
from .handle_uploads import registration_upload, participant_upload
from .handle_relationships import participated_tf
from .models import ExcludedIndividual, MasterDB
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .data_processing.processing_file import data_cleaning
from .master_to_db.master_to_db import master_to_db

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'Username or password is incorrect')

            return render(request, 'dashboard/login.html')

    return render(request, 'dashboard/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login')
def home(request):
    if request.method == "POST":
        participant_files = request.FILES.getlist('participant_files')
        registration_files = request.FILES.getlist('registration_files')
        registration_file = registration_files[0]
        participant_file = participant_files[0]
        master_df = data_cleaning(registration_file, participant_file)
        master_to_db(master_df)



    data = MasterDB.objects.all().values(
        'topic', 'event_date', 'first_name', 'last_name', 'email', 'registration_time', 'join_time', 'leave_time', 'duration', 'attended'
    )

    data_json = json.dumps(list(data))
    excludedEmailsDB = json.dumps(list(ExcludedIndividual.objects.all().values('email')))

    context = {'excludedEmailsDB':excludedEmailsDB, 'data_json': data_json}
    return render(request, 'dashboard/home.html', context)



def excluded_emails(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        emails = body_data.get('emails', [])
        ExcludedIndividual.objects.all().delete()
        for email in emails:
            ExcludedIndividual.objects.create(email=email)
        Registration.objects.filter(email__in=emails).delete()
        Participant.objects.filter(email__in=emails).delete()
        return HttpResponse('Excluded emails updated successfully', status=200)

@login_required(login_url='/login')
def comparison(request):
    return render(request, 'dashboard/comparison.html')

@login_required(login_url='/login')
def visualization(request):
    return render(request, 'dashboard/visualization.html')

