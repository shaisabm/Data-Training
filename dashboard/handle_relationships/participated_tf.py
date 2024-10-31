# from dashboard.models import Registration
# from dashboard.models import Participant
# import pandas as pd
# def participated_tf(registration_files):
#
#     for registration_file in registration_files:
#         df = pd.read_excel(registration_file)
#
#         name_text = registration_file.name.split('_')
#         for i in name_text:
#             if len(i) == 11 and i.isdigit():
#                 zoom_id = i
#
#         register_details = df.iloc[5:, :5]
#
#         for index, row in register_details.iterrows():
#             email = row.iloc[2]
#             if Participant.objects.filter( zoom_id=zoom_id, email=email).exists():
#                 Registration.objects.filter( zoom_id=zoom_id, email=email).update(participated=True)
