# from datetime import datetime
#
# from django.utils import timezone
# import pandas as pd
# from dashboard.models import Registration, ExcludedIndividual
#
#
# def registration_upload(registration_files):
#     zoom_id = None
#     excluded_emails = ExcludedIndividual.get_all_emails()
#     for registration_file in registration_files:
#         df = pd.read_excel(registration_file)
#         event_name = df.iloc[2, 0]
#         name_text = registration_file.name.split('_')
#         for i in name_text:
#             if len(i) == 11 and i.isdigit():
#                 zoom_id = i
#
#         register_details = df.iloc[5:, :5]
#
#         for index, row in register_details.iterrows():
#             first_name = row.iloc[0]
#             last_name = row.iloc[1]
#             email = row.iloc[2]
#             date ,_= str((row.iloc[3])).split(" ")
#             registration_time = date
#             approval_status = row.iloc[4]
#             if "@nyit.edu" in email and email not in excluded_emails:
#
#                 Registration.objects.update_or_create(
#                     zoom_id=zoom_id,
#                     email=email,
#                     defaults={
#                         'event_name': event_name,
#                         'first_name': first_name,
#                         'last_name': last_name,
#                         'registration_time': registration_time,
#                         'approval_status': approval_status
#                     }
#                 )
#
#
#
