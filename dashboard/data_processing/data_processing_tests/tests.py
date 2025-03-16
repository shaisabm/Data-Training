# import os
# import pandas as pd
# import re
#
# # input and output folders
# folders = {
#
# # May
#     'participants': '/Users/shaisabm/Downloads/',
#     'registration': '/Users/shaisabm/Downloads/',
#     'master_file': '/Users/shaisabm/Documents/Django/DataTraining/dashboard/data_processing/data_processing_tests/master'
# }
#
# # Ensure output directory exists
# os.makedirs(folders['master_file'], exist_ok=True)
#
#
# ### Standardize Column Names ###
# def standardize_columns(data):
#     # Convert all column names to lowercase and rename variations
#     data.columns = data.columns.str.lower()
#     rename_dict = {
#         'user email': 'email', 'email': 'email',
#         'name (original name)': 'name', 'name (original name)': 'name',
#         'join time': 'join time', 'leave time': 'leave time',
#         'duration (minutes)': 'duration', 'guest': 'guest',
#         'in waiting room': 'in waiting room'
#     }
#     data.rename(columns=rename_dict, inplace=True)
#     return data
#
#
# ### 1: Clean Participant Data ###
# def clean_participant_data(data):
#     # Standardize columns
#     data = standardize_columns(data)
#
#     # Sort by duration and drop duplicates by email
#     data.sort_values(by='duration', ascending=False, inplace=True)
#     data.drop_duplicates(subset='email', keep='first', inplace=True)
#
#     # Filter by email domain and guests
#     is_nyit_email = data['email'].str.endswith('@nyit.edu')
#     is_guest = data['guest'] == 'Yes'
#     data = data[is_nyit_email | is_guest]
#     data = data[data['email'] != 'jlawlor@nyit.edu']
#     data = data[data['duration'] >= 2]
#     return data
#
#
# ### 2: Extract Topic, ID, and Event Date from Registration Data ###
# def extract_precise_topic_id(file_path):
#     with open(file_path, 'r') as file:
#         raw_content = file.readlines()
#     topic_data = []
#     for line in raw_content:
#         split_line = line.strip().split(",")
#         if len(split_line) >= 2 and split_line[1].strip().replace(" ", "").isdigit():
#             topic = split_line[0].strip()
#             topic_id = split_line[1].strip()
#             scheduled_time = split_line[2].strip().replace('"', '')[:10] if len(split_line) > 2 else ""
#             topic_data.append([topic, topic_id, scheduled_time])
#     topic_df = pd.DataFrame(topic_data, columns=["topic", "id", "event date"])
#     return topic_df
#
#
# ### 3: Extract Attendee Names and Details from Registration Data ###
# def clean_attendee_data(file_path):
#     with open(file_path, 'r') as file:
#         raw_content = file.readlines()
#     attendee_data = []
#     capture_attendees = False
#     for line in raw_content:
#         # Start capturing attendees if "Attendee Details" is found or if columns start with 'First Name'
#         if "Attendee Details" in line:
#             capture_attendees = True
#             continue
#         elif any(col_name in line.lower() for col_name in ['first name', 'last name', 'email']):
#             capture_attendees = True
#
#         if capture_attendees:
#             split_line = line.strip().split(",")
#             if len(split_line) >= 5:
#                 attendee_info = split_line[:5]
#                 attendee_data.append(attendee_info)
#
#     # Convert collected attendee data to a DataFrame
#     attendee_df = pd.DataFrame(attendee_data,
#                                columns=["first name", "last name", "email", "registration time", "approval status"])
#     # Standardize columns
#     attendee_df = standardize_columns(attendee_df)
#
#     # Remove duplicates and filter by NYIT emails
#     attendee_df.drop_duplicates(subset="email", inplace=True)
#     attendee_df = attendee_df[attendee_df["email"].str.endswith("@nyit.edu")]
#     return attendee_df
#
#
# ### 4: Process Each Participant and Registration File, Merge, and Accumulate Data ###
# all_data = []
# participant_ids = set()
#
# # 4.1: Process Participants Data and store their IDs
# print("Processing participant files...")
# for filename in os.listdir(folders['participants']):
#     if filename.startswith('participants_') and filename.endswith('.csv'):
#         participant_id = re.search(r'participants_(\d+)', filename)
#         if participant_id:
#             participant_id = participant_id.group(1)
#             participant_ids.add(participant_id)
#             print(f"Processing participant file: {filename} with ID: {participant_id}")
#
#             # Load participant data
#             participant_data = pd.read_csv(os.path.join(folders['participants'], filename))
#             participant_data = standardize_columns(participant_data)
#             print(f"Rows in participant data ({filename}): {len(participant_data)}")
#
#             cleaned_participant_data = clean_participant_data(participant_data)
#
#             # Find matching registration file by ID
#             reg_filename_pattern = f'registration_{participant_id}_\\d+_\\d+_\\d+\\.csv'
#             matched_files = [f for f in os.listdir(folders['registration']) if re.match(reg_filename_pattern, f)]
#
#             if matched_files:
#                 reg_filename = matched_files[0]
#                 reg_filepath = os.path.join(folders['registration'], reg_filename)
#                 print(f"Matching registration file found: {reg_filename}")
#
#                 # Attempt to extract Topic, ID, and Event Date from Registration Data
#                 try:
#                     reg_topic_data = extract_precise_topic_id(reg_filepath)
#                     # If reg_topic_data is empty, set default values for missing fields
#                     if reg_topic_data.empty:
#                         reg_topic_data = pd.DataFrame({'topic': [""], 'id': [""], 'event date': [""]})
#                 except:
#                     # If extraction fails, set default values
#                     reg_topic_data = pd.DataFrame({'topic': [""], 'id': [""], 'event date': [""]})
#
#                 # Extract Attendee Data
#                 cleaned_attendee_data = clean_attendee_data(reg_filepath)
#                 print(f"Rows in attendee data ({reg_filename}): {len(cleaned_attendee_data)}")
#
#                 # Merge cleaned_attendee_data with cleaned_participant_data on 'email'
#                 merged_data = pd.merge(
#                     cleaned_attendee_data, cleaned_participant_data, on='email', how='outer', indicator=True
#                 )
#
#                 # Add Registration Data and Participant Data indicators for unmatched emails
#                 merged_data['registration data'] = merged_data.apply(
#                     lambda row: row['email'] if row['_merge'] == 'left_only' else None, axis=1
#                 )
#                 merged_data['participant data'] = merged_data.apply(
#                     lambda row: row['email'] if row['_merge'] == 'right_only' else None, axis=1
#                 )
#                 merged_data['attended'] = merged_data['registration data'].apply(
#                     lambda x: 'No' if pd.notnull(x) else 'Yes')
#                 merged_data.drop(columns=['_merge'], inplace=True)
#
#                 # Add Topic, ID, and Event Date columns uniformly to each row
#                 for col in ["topic", "id", "event date"]:
#                     merged_data[col] = reg_topic_data[col].iloc[0] if col in reg_topic_data else ""
#
#                 # Append the processed data to all_data list
#                 all_data.append(merged_data)
#                 print(f"Appended data for participant ID: {participant_id}")
#             else:
#                 print(f"No matching registration file found for participant ID: {participant_id}")
#
# # Check if all_data contains any data before proceeding to concatenate
# if all_data:
#     ### 5: Concatenate All Data and Sort ###
#     master_df = pd.concat(all_data, ignore_index=True)
#     master_df = master_df[['topic', 'id', 'event date', 'first name', 'last name', 'email',
#                            'registration time', 'approval status', 'join time', 'leave time',
#                            'duration', 'guest', 'attended']]
#     master_df['event date'] = pd.to_datetime(master_df['event date'], format='%m/%d/%Y', errors='coerce')
#     master_df = master_df.sort_values(by='event date')
#     master_df['event date'] = master_df['event date'].dt.strftime('%m/%d/%Y')
#
#     # 6: Save Final Master File
#     output_file_path = os.path.join(folders['master_file'], 'Master_Attendance_File.csv')
#     master_df.to_csv(output_file_path, index=False)
#     print(f"Master file saved: {output_file_path}")
# else:
#     print("No data found to process. Please check input folders.")

import json
from jsonschema import validate

# Describe what kind of json you expect.
schema = {
    "type" : "object",
    "properties" : {
        "description" : {"type" : "string"},
        "status" : {"type" : "boolean"},
        "value_a" : {"type" : "number"},
        "value_b" : {"type" : "number"},
    },
}

# Convert json to python object.
my_json = json.loads('{"description": "Hello world!", "status": true, "value_a": 1, "value_b": 3.14}')

# Validate will raise exception if given json is not
# what is described in schema.
validate(instance=my_json, schema=schema)

# print for debug
print(my_json)