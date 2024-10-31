
from dashboard.models import ExcludedIndividual, MasterDB


def master_to_db(master_df):

    for index, row in master_df.iterrows():
        if str(row['duration']) == 'nan':
            duration = 0
            print('duration is nan')
        else:
            duration = row['duration']

        email = row['email']
        if ExcludedIndividual.objects.filter(email=email).exists():
            continue
        MasterDB.objects.update_or_create(
            topic = row['topic'],
            zoom_id = row['id'],
            event_date = row['event date'],
            first_name = row['first name'],
            last_name = row['last name'],
            email = row['email'],
            registration_time = row['registration time'],
            join_time = row['join time'],
            leave_time = row['leave time'],
            duration = duration,
            attended = row['attended']
        )
