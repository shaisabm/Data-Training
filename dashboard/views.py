import json
from django.shortcuts import render
from .handle_uploads import registration_upload, participant_upload
from .handle_relationships import participated_tf
from .models import Registration, Participant, ExcludedIndividual
from django.http import HttpResponse


def home(request):
    if request.method == "POST":
        participant_files = request.FILES.getlist('participant_files')
        registration_files = request.FILES.getlist('registration_files')

        registration_upload.registration_upload(registration_files)
        participant_upload.participant_upload(participant_files)
        participated_tf.participated_tf(registration_files)

    registrations = Registration.objects.all().values(
        'event_name', 'zoom_id', 'first_name', 'last_name', 'email', 'registration_time', 'approval_status', 'participated'
    )
    registration_data = list(registrations)
    registration_data_json = json.dumps(registration_data)

    participation = Participant.objects.all().values(
        'event_name', 'zoom_id', 'full_name', 'email', 'joined_time', 'leave_time', 'duration', 'guest', 'in_waiting_room'
    )
    participant_data = [
        {
            **item,
            'joined_time': item['joined_time'].isoformat(),
            'leave_time': item['leave_time'].isoformat()
        }
        for item in participation
    ]
    participant_data_json = json.dumps(participant_data)

    excludedEmailsDB = json.dumps(list(ExcludedIndividual.objects.all().values('email')))

    context = {'registration_data_json': registration_data_json, 'participant_data_json': participant_data_json, 'excludedEmailsDB':excludedEmailsDB}
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


def comparison(request):
    return render(request, 'dashboard/comparison.html')

def visualization(request):
    return render(request, 'dashboard/visualization.html')

