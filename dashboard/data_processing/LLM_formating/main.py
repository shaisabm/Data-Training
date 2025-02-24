from openai import OpenAI
import pandas as pd
import os
import time


class ModelConfig:
    def __init__(self, ai_model, api_key, base_url, system_instructions):
        self.ai_model = ai_model
        self.api_key = api_key
        self.base_url = base_url
        self.system_instructions = system_instructions


def open_ai(registration, participants, model, model_config):
    client = OpenAI(
        api_key=model_config['api_key'],
        base_url=model_config['base_url']
    )

    df_registration = pd.read_csv(registration)
    registration_content = df_registration.to_string()

    df_participants = pd.read_csv(participants)
    participants_content = df_participants.to_string()

    completion = client.chat.completions.create(

        model=model.ai_model,
        messages=[
            {
                "role": "system",
                "content": model_config['system_instructions']
            },
            {
                "role": "user",
                "content": f"Registration Content:\n{registration_content}\n\nParticipants Content:\n{participants_content}"
            }
        ]
    )

    return  completion.choices[0].message.content


system_instructions = """You are a data formatting assistant. Your task is to convert input data into a specific JSON format.
Follow these strict formatting rules:
1. Output must be valid JSON
2. Remove all newlines from the output
3. Participants should be an array of objects containing ALL registrants
4. Follow this exact structure:

                     {
                         "event": {
                             "topic": string,
                             "id": integer,
                             "event_month": word form,
                             "event_date": "m/d/yyyy",
                             "event_time": string
                         },
                         "participants": [{
                             "first_name": string,
                             "last_name": string,
                             "email": string,
                             "duration": integer,
                             "join_time": string,
                             "leave_time": string,
                             "attended": Yes/No
                         },
                         {
                         ... additional participants ...
                        }]
                     }
Important Rules:
1. Participant Processing:
- Include ALL people from the registration list in the participants array
- Match participants data using email addresses
- For registrants who didn't attend (not in participants list):
* Set duration to 0
* Set join_time and leave_time to null
* Set attended to false
- No duplicate participants (use email as unique identifier)
- If multiple entries exist for same email in participants list, add the durations

2. Time Format Requirements:
- event_time format: "HH:MM:SS AM/PM" (e.g., "10:00:00 AM")
- join_time format: "M/D/YYYY HH:MM:SS AM/PM" (e.g., "8/14/2024 1:30:42 PM")
- leave_time format: "M/D/YYYY HH:MM:SS AM/PM" (e.g., "8/14/2024 1:30:42 PM")
- All times must include seconds
- Use 12-hour format with AM/PM

3. Attendance Rules:
- 'attended' is Yes ONLY if:
* Person appears in the participants list AND
* Has duration >= 5 minutes
- 'attended' is No otherwise

4. Time Handling:
- If join_time is missing but person attended, use event start time with event date
- If leave_time is missing but person attended, use event end time with event date
- For non-attendees, use null for both join_time and leave_time

5. Data Consistency:
- Maintain consistent formatting for all participant entries
- Duration should be in minutes (integer)
- Email addresses should be lowercase
- For event time always include leading zeros in hours (e.g., "09:00:00 AM" not "9:00:00 AM")
- For join/leave time don't include leading zeros in hours (e.g., "8:00:00 AM" not "08:00:00 AM")
- Always include seconds even if they're 00"""

reg = "/Users/shaisabm/Documents/Django/DataTraining/dashboard/data_processing/LLM_formating/93654500555_RegistrationReport(in).csv"
part = "/Users/shaisabm/Documents/Django/DataTraining/dashboard/data_processing/LLM_formating/participants_93654500555(in).csv"

model_config = [
    ModelConfig(
    "google/gemini-2.0-flash-thinking-exp:free",
    "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",
    "https://openrouter.ai/api/v1",
    system_instructions),
    # ModelConfig(
    #     "google/gemini-2.0-pro-exp-02-05:free",
    #     "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",
    #     "https://openrouter.ai/api/v1",
    #     system_instructions),
    ModelConfig(
        "google/gemini-2.0-flash-exp:free",
        "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",
        "https://openrouter.ai/api/v1",
        system_instructions),

]
# for model in model_config:
#     start_time = time.time()
#     open_ai(reg, part, model)
#     end_time = time.time()
#
#     execution_time = end_time - start_time
#     print(f" {model.ai_model} Execution time: {execution_time} seconds")


