import json

from django.shortcuts import render, redirect

from .models import ExcludedIndividual, MasterDB
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .data_processing.processing_file import data_cleaning
from .master_to_db.master_to_db import master_to_db
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.response import Response
from rest_framework.decorators import api_view


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
        try:
            participant_files = request.FILES.getlist('participation_files')
            del request.FILES['participation_files']
        except:
            participant_files = []

        request_dict = dict(request.FILES)

        registration_files = []
        for key in request.FILES.keys():
            for file in request_dict[key]:
                base_name = str(file).split('_')[:2]
                new_file = InMemoryUploadedFile(
                    file=file,
                    field_name=file.field_name,
                    name=f"{base_name[0]}_{base_name[1]}_{key}.csv",
                    content_type=file.content_type,
                    size=file.size,
                    charset=file.charset,
                    content_type_extra=file.content_type_extra

                )
                registration_files.append(new_file)

        participant_dict = {str(participant_file).split('_')[1][:11]: participant_file for participant_file in
                            participant_files}
        registration_dict = {}
        for f in registration_files:
            id = str(f).split('_')[1]
            registration_dict[id] = f

        keys_to_remove = []
        for r_key in registration_dict.keys():
            if r_key not in participant_dict.keys():
                keys_to_remove.append(r_key)


        for p_key in participant_dict.keys():
            if p_key not in registration_dict.keys():
                keys_to_remove.append(p_key)

        for key in keys_to_remove:
            if (key in registration_dict.keys()):
                registration_dict.pop(key)
            if (key in participant_dict.keys()):
                participant_dict.pop(key)

        for key in registration_dict.keys():
            registration_file = registration_dict[key]
            participant_file = participant_dict[key]
            master_df = data_cleaning(registration_file, participant_file)
            master_to_db(master_df)

    data = MasterDB.objects.all().values(
        'topic', 'event_date', 'first_name', 'last_name', 'email', 'registration_time', 'join_time', 'leave_time',
        'duration', 'attended'
    )

    data_json = json.dumps(list(data))
    excludedEmailsDB = json.dumps(list(ExcludedIndividual.objects.all().values('email')))
    context = {'excludedEmailsDB': excludedEmailsDB, 'data_json': data_json}
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


@api_view(['POST'])
def get_missing_files(request):
    participant_files = request.data['participations']
    registration_files = request.data['registrations']
    participant_dict = {str(participant_file).split('_')[1][:11]: participant_file for participant_file in
                        participant_files}

    registration_dict = {str(f).split('_')[1]: f for f in registration_files}
    missing_files = set()

    for r_key in registration_dict.keys():
        if r_key not in participant_dict.keys():
            missing_files.add("Participation file is missing for " + registration_dict[r_key])

    for p_key in participant_dict.keys():
        if p_key not in registration_dict.keys():
            missing_files.add(f'Registration file is missing for {participant_dict[p_key]}')
    print(missing_files)
    return Response({'missing_files': list(missing_files)}, status=200)
