import pandas as pd
from io import StringIO
import calendar
import os
from datetime import datetime

def data_cleaning(registration_file, participant_file):

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
                scheduled_time = split_line[2].strip().replace('"', '') #[:10] if len(split_line) > 2 else ""
                dt = datetime.strptime(scheduled_time,'%m/%d/%Y %H:%M')

                date_str = dt.strftime('%m/%d/%Y')
                time_str = dt.strftime('%I:%M %p')
                month_str = dt.strftime('%B')

                topic_data.append([topic, topic_id, month_str, date_str, time_str])
        topic_df = pd.DataFrame(topic_data, columns=["topic", "id", "event month", "event date", "event time"])
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
        month = (filename.split('_')[2]).split('.')[0]
        if month:
            return calendar.month_name[int(month)]
        return ""

    # Process participant and registration files in-memory
    participant_data = pd.read_csv(StringIO(participant_file.read().decode('utf-8')))
    cleaned_participant_data = clean_participant_data(participant_data)

    registration_content = registration_file.read().decode('utf-8')
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

    for col in ["topic", "id", "event month", "event date", "event time"]:
        merged_data[col] = reg_topic_data[col].iloc[0] if col in reg_topic_data else ""

    merged_data["event month"] = event_date

    all_data = [merged_data]

    if all_data:
        master_df = pd.concat(all_data, ignore_index=True)
        master_df = master_df[['topic', 'id', 'event month', 'event date', 'event time', 'first name', 'last name', 'email',
                               'registration time', 'approval status', 'join time', 'leave time',
                               'duration', 'guest', 'attended']]

        # Commented are the lines which were used to convert the date format to 'mm/dd/yyyy'
        # master_df['event date'] = pd.to_datetime(master_df['event date'], format='%m/%d/%Y', errors='coerce')
        # master_df = master_df.sort_values(by='event date')
        # master_df['event date'] = master_df['event date'].dt.strftime('%m/%d/%Y')

        ## TEST -- MUST BE DELETED IN PRODUCTION

        # 6: Save Final Master File
        # file_path = "/Users/shaisabm/Documents/Django/DataTraining/dashboard/data_processing/data_processing_tests/master"
        # output_file_path = os.path.join(file_path, 'Master_Attendance_File.csv')
        # master_df.to_csv(output_file_path, index=False)
        # print(f"Master file saved: {output_file_path}")

        return master_df
    else:
        print("No data found to process. Please check input folders.")