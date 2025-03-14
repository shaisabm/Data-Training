import json
from django.shortcuts import render, redirect
from .models import ExcludedIndividual, MasterDB, AiModel
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .spreadsheet_processing.main import match_registration_participant_files
from .spreadsheet_processing.celery_worker import process_ai_models_async, save_for_celery
from celery import shared_task

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
            return render(request, 'dashboard/login.html')
    return render(request, 'dashboard/login.html')


def logout_user(request):
    logout(request)
    print("Logged out successfully")
    return redirect('login')

@login_required(login_url='/login')
def home(request):


    if request.method == "POST":

        registration_files = dict(request.FILES).setdefault("registration_files", None)
        participant_files = dict(request.FILES).setdefault("participant_files", None)

        matched_pairs = match_registration_participant_files(registration_files, participant_files)['matched_pairs']
        missing_files = match_registration_participant_files(registration_files, participant_files)['missing_files']


        n = len(matched_pairs)
        for i in range(n):
            pair = matched_pairs[i]
            reg_data = save_for_celery(pair[0])
            part_data = save_for_celery(pair[1])
            matched_pairs[i] = (reg_data, part_data, pair[0].name)
        process_ai_models_async.delay(matched_pairs)

    data = MasterDB.objects.all().values(
        'topic', 'zoom_id', 'event_date', 'first_name', 'last_name', 'email', 'join_time', 'leave_time',
        'duration', 'attended'
    )

    data_json = json.dumps(list(data))
    excluded_emailsDB = json.dumps(list(ExcludedIndividual.objects.all().values('email')))
    context = {'excludedEmailsDB': excluded_emailsDB, 'data_json': data_json}
    return render(request, 'dashboard/home.html', context)


def excluded_emails(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        emails = body_data.get('emails', [])
        ExcludedIndividual.objects.all().delete()
        for email in emails:
            ExcludedIndividual.objects.create(email=email)
        MasterDB.objects.filter(email__in=emails).delete()
        return HttpResponse('Excluded emails updated successfully', status=200)


@login_required(login_url='/login')
def comparison(request):
    return render(request, 'dashboard/comparison.html')


@login_required(login_url='/login')
def visualization(request):
    return render(request, 'dashboard/visualization.html')



