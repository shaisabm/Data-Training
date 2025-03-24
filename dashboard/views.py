import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect
from .models import ExcludedIndividual, MasterDB
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .spreadsheet_processing.main import match_reg_part_files
from .spreadsheet_processing.tasks import process_ai_models_async, save_for_celery
from django.contrib.auth.models import User


def login_user(request):
    """
    Handle user login.
    Redirects to home if user is already authenticated.
    Processes login form submission and authenticates users.
    """

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
    """
    Handle user logout and redirect to login page.
    """
    logout(request)
    print("Logged out successfully")
    return redirect('login')


@login_required(login_url='/login')
def home(request):
    """
    Main dashboard view that handles:
    1. File uploads and processing via POST request
    2. Display of attendance data via GET request

    Uses PRG pattern to avoid form resubmission on refresh.
    """
    if request.method == "POST":

        # Extract uploaded files from request
        reg_files = dict(request.FILES).setdefault("registration_files", None)
        part_files = dict(request.FILES).setdefault("participant_files", None)

        # Match registration and participant files
        reg_part_files = match_reg_part_files(reg_files, part_files)
        matched_pairs, missing_files = reg_part_files['matched_pairs'], reg_part_files['missing_files']

        for file in missing_files:
            messages.warning(request, "Missing: " + file)

        # Process matched pairs for asynchronous processing
        n = len(matched_pairs)
        for i in range(n):
            pair = matched_pairs[i]
            reg_data = save_for_celery(pair[0])
            part_data = save_for_celery(pair[1])
            matched_pairs[i] = (reg_data, part_data, pair[0].name)

        # Only trigger async processing if matches were found
        if len(matched_pairs) != 0:
            process_ai_models_async.delay(matched_pairs)
        return redirect('home')

    # Prepare data for JavaScript
    data = MasterDB.objects.all().values(
        'topic', 'zoom_id', 'event_date', 'first_name', 'last_name', 'email', 'join_time', 'leave_time',
        'duration', 'attended'
    )

    data_json = json.dumps(list(data))
    excluded_emailsDB = json.dumps(list(ExcludedIndividual.objects.all().values('email')))
    context = {'excludedEmailsDB': excluded_emailsDB, 'data_json': data_json}
    return render(request, 'dashboard/home.html', context)


def excluded_emails(request):
    """
    API endpoint to update excluded email list.
    Deletes all existing excluded emails and adds new ones from POST data.
    Also removes matching records from MasterDB.
    """
    if request.method == 'POST':

        # Parse JSON data from request body
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        emails = body_data.get('emails', [])

        # Clear existing excluded emails and add new ones
        ExcludedIndividual.objects.all().delete()
        for email in emails:
            ExcludedIndividual.objects.create(email=email.lower())

        # Remove excluded individuals from master database
        MasterDB.objects.filter(email__in=emails).delete()
        return HttpResponse('Excluded emails updated successfully', status=200)


@login_required(login_url='/login')
def comparison(request):
    """
    Display comparison view (protected by login).
    """
    return render(request, 'dashboard/comparison.html')


@login_required(login_url='/login')
def visualization(request):
    """
    Display visualization view (protected by login).
    """
    return render(request, 'dashboard/visualization.html')


def test(request, pk):
    """
    Test endpoint to render the master table component.
    """

    user = User.objects.filter(pk=pk).first()
    if user is None or user.pk != request.user.pk:
        return redirect('login')


    return render(request, "dashboard/logs.html", {'pk': pk})
