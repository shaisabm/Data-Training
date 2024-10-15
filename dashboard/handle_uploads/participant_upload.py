from django.utils import timezone
import pandas as pd
from dashboard.models import Registration, Participant
import re


def participant_upload(participant_files):
    for participant_file in participant_files:

        df = pd.read_excel(participant_file)
        name_text = re.split(r'[_\.]', participant_file.name)

        zoom_id = None
        for i in name_text:
            if len(i) == 11 and i.isdigit():
                zoom_id = i
        event_name = Registration.objects.filter(zoom_id=zoom_id).first().event_name

        participant_details = df.iloc[1:, :7]
        for index, row in participant_details.iterrows():
            full_name = row.iloc[0]
            email = row.iloc[1]
            joined_time = timezone.make_aware(row.iloc[2])
            leave_time = timezone.make_aware(row.iloc[3])
            duration = row.iloc[4]
            guest = row.iloc[5]
            in_waiting_room = row.iloc[6]
            if duration < 5:
                continue
            if Participant.objects.filter(zoom_id=zoom_id, email=email).exists():
                previous_participant = Participant.objects.filter(zoom_id=zoom_id, email=email).first()
                if previous_participant.duration < duration:
                    previous_participant.duration = duration
                    previous_participant.save()
            else:
                Participant.objects.update_or_create(
                    zoom_id=zoom_id,
                    email=email,
                    defaults={
                        'event_name': event_name,
                        'full_name': full_name,
                        'joined_time': joined_time,
                        'leave_time': leave_time,
                        'duration': duration,
                        'guest': guest == 'Yes',
                        'in_waiting_room': in_waiting_room == 'Yes'
                    }
                )

