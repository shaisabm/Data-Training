import pandas as pd
from io import StringIO
import os
import re

def data_cleaning(registration_file, participant_file):
    # os.makedirs(folders['master_file'], exist_ok=True)

    def standardize_columns(data):
        data.columns = data.columns.str.lower()
        rename_dict = {
            'user email': 'email', 'email': 'email',
            'name (original name)': 'name', 'name (original name)': 'name',
            'join time': 'join time', 'leave time': 'leave time',
            'duration (minutes)': 'duration', 'guest': 'guest',
            'in waiting room': 'in waiting room'
        }
        data.rename(columns=rename_dict, inplace=True)
        return data

    def clean_participant_data(data):
        data = standardize_columns(data)
        data.sort_values(by='duration', ascending=False, inplace=True)
        data.drop_duplicates(subset='email', keep='first', inplace=True)

        is_nyit_email = data['email'].str.endswith('@nyit.edu')
        is_guest = data['guest'] == 'Yes'
        data = data[is_nyit_email | is_guest]
        data = data[data['email'] != 'jlawlor@nyit.edu']
        data = data[data['duration'] >= 2]
        return data

    def extract_precise_topic_id(file_content):
        raw_content = file_content.splitlines()
        topic_data = []
        for line in raw_content:
            split_line = line.strip().split(",")
            if len(split_line) >= 2 and split_line[1].strip().replace(" ", "").isdigit():
                topic = split_line[0].strip()
                topic_id = split_line[1].strip()
                scheduled_time = split_line[2].strip().replace('"', '')[:10] if len(split_line) > 2 else ""
                topic_data.append([topic, topic_id, scheduled_time])
        topic_df = pd.DataFrame(topic_data, columns=["topic", "id", "event date"])
        return topic_df

    def clean_attendee_data(file_content):
        raw_content = file_content.splitlines()
        attendee_data = []
        capture_attendees = False
        for line in raw_content:
            if "Attendee Details" in line:
                capture_attendees = True
                continue
            elif any(col_name in line.lower() for col_name in ['first name', 'last name', 'email']):
                capture_attendees = True

            if capture_attendees:
                split_line = line.strip().split(",")
                if len(split_line) >= 5:
                    attendee_info = split_line[:5]
                    attendee_data.append(attendee_info)

        attendee_df = pd.DataFrame(attendee_data,
                                   columns=["first name", "last name", "email", "registration time", "approval status"])
        attendee_df = standardize_columns(attendee_df)
        attendee_df.drop_duplicates(subset="email", inplace=True)
        attendee_df = attendee_df[attendee_df["email"].str.endswith("@nyit.edu")]
        return attendee_df

    def extract_event_date_from_filename(filename):
        match = re.search(r'registration_\d+_(\d{4})_(\d{2})_(\d{2})', filename)
        if match:
            year, month, day = match.groups()
            return f"{month}/{day}/{year}"
        return ""


    # Process participant and registration files in-memory
    participant_data = pd.read_csv(StringIO(participant_file.read()))
    cleaned_participant_data = clean_participant_data(participant_data)

    registration_content = registration_file.read()
    reg_topic_data = extract_precise_topic_id(registration_content)
    cleaned_attendee_data = clean_attendee_data(registration_content)

    event_date = extract_event_date_from_filename(registration_file.name)

    merged_data = pd.merge(
        cleaned_attendee_data, cleaned_participant_data, on='email', how='outer', indicator=True
    )
    merged_data['registration data'] = merged_data.apply(
        lambda row: row['email'] if row['_merge'] == 'left_only' else None, axis=1
    )
    merged_data['participant data'] = merged_data.apply(
        lambda row: row['email'] if row['_merge'] == 'right_only' else None, axis=1
    )
    merged_data['attended'] = merged_data['registration data'].apply(
        lambda x: 'No' if pd.notnull(x) else 'Yes')
    merged_data.drop(columns=['_merge'], inplace=True)

    for col in ["topic", "id", "event date"]:
        merged_data[col] = reg_topic_data[col].iloc[0] if col in reg_topic_data else ""

    merged_data["event date"] = event_date

    all_data = [merged_data]

    if all_data:
        master_df = pd.concat(all_data, ignore_index=True)
        master_df = master_df[['topic', 'id', 'event date', 'first name', 'last name', 'email',
                               'registration time', 'approval status', 'join time', 'leave time',
                               'duration', 'guest', 'attended']]
        master_df['event date'] = pd.to_datetime(master_df['event date'], format='%m/%d/%Y', errors='coerce')
        master_df = master_df.sort_values(by='event date')
        master_df['event date'] = master_df['event date'].dt.strftime('%m/%d/%Y')

        code = re.search(r'(\d{11})', registration_file.name).group(1)
        output_file_path = os.path.join('/dashboard/not_in_use_data_processing/master', f'{code}.csv')
        master_df.to_csv(output_file_path, index=False)
        print(f"Master file saved: {output_file_path}")

        return master_df
    else:
        print("No data found to process. Please check input folders.")




# with open('2024 August Training Attendance/87', 'r') as reg, open('2024 August Training Attendance/participants_91296104245.csv') as part:
#     data_cleaning(reg, part)
from os import listdir
from os.path import isfile, join

part = {}
reg = {}


path = "2024 August Training Attendance/"

for f in listdir(path):
    code = re.search(r'(\d{11})', f).group(1)
    if "participants" in f:
        part[code] = f
    else:
        reg[code] = f


common_code = set(part.keys() & reg.keys())

print(common_code)
for c in common_code:
    reg_file = f"2024 August Training Attendance/{reg[c]}"
    part_file = f"2024 August Training Attendance/{part[c]}"
    with open(reg_file, 'r') as r, open(part_file) as p:
        data_cleaning(r, p)

